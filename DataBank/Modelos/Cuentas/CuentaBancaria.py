from .Cliente import Cliente
from DataBank.Modelos.Cuentas.transaccion import Transaction
from Modelos.Excepciones.SaldoInsuficienteException import SaldoInsuficienteException
from Modelos.Excepciones.OperacionImposibleException import OperacionImposibleException
from DataBank.Modelos.Cuentas.tarjeta import Card
import uuid
from datetime import datetime
from datetime import timedelta

class CuentaBancaria:
    recuento_cuentas: int = 0

    def __init__(self, numero_bancario: int, cliente: Cliente, numero_de_cuenta: int | None = None):
        if numero_bancario is None or numero_bancario <= 0:
            raise ValueError("Es obligatorio un número de agencia válido")
        if numero_de_cuenta is not None and numero_de_cuenta <= 0:
            raise ValueError("Es obligatorio ingresar el número de cuenta")

        self.numero_bancario = numero_bancario
        self.numero_de_cuenta = (
            numero_de_cuenta if numero_de_cuenta is not None
            else str(uuid.uuid4())[:8]
        )
        self.cliente = cliente
        self._balance: float = 0.0
        self.tasa_interes: float = 0.0
        self.sobregiro_limite: float = 0.0
        self.cuenta_activa: bool = False
        self.valor_comision: float = 0.0
        self.__retiros_sin_balance: int = 0
        self.__transferencia_sin_balance: int = 0
        self.transacciones: list["Transaction"] = []
        self.maximo_transacciones_por_minuto = 1
        self.fecha_creacion = datetime.now()
        self.tarjetas: list["Card"] = []
        self.bloqueado_hasta: datetime | None = None

        CuentaBancaria.recuento_cuentas += 1

    def obtener_balance(self) -> float:
        return self._balance

    def obtener_retiros_sin_balance(self) -> int:
        return self.__retiros_sin_balance

    def obtener_transferencias_sin_balance(self) -> int:
        return self.__transferencia_sin_balance
    
    def obtener_minimo_balance(self)-> float:
        return 0

    def obtener_maximo_transacciones_por_minuto(self):
        return self.maximo_transacciones_por_minuto
    
    def puede_retirar(self, monto: float)-> bool:
        if self._balance - monto < self.obtener_minimo_balance():
            return False
        return True
    
    def retiros_diarios(self):
        hoy = datetime.now().date()
        return [
        t for t in self.transacciones
        if t.type == "Retiro" and t.date.date() == hoy
        ]
    
    def verificar_limite_transacciones(self):
        now = datetime.now()
        hace_un_minuto = now - timedelta(minutes=1)

        reciente = [
            t for t in self.transacciones
            if t.date >= hace_un_minuto
        ]

        if len(reciente) >= self.obtener_maximo_transacciones_por_minuto():
            raise OperacionImposibleException("Límite excedido")

    def retirar(self, monto: float) -> bool:
        if self.esta_temporalmente_bloqueado():
            raise OperacionImposibleException("La cuenta está bloqueada temporalmente.")
    
        self.verificar_limite_transacciones()
        
        if monto <= 0:
            raise ValueError("Monto inválido")

        if not self.puede_retirar(monto):
            self.__retirar_sin_balance += 1
            raise SaldoInsuficienteException("No puede superar el límite de la cuenta")

        self._balance -= monto
        retirar = self.transacciones(type="Retiro", monto = monto, cuenta_de_origen =self, cuenta_de_destino = None, descripcion =f"Retiro de: ${monto}")
        self.transacciones.append(retirar)
        return True

    def deposito(self, monto: float) -> None:
        if self.esta_temporalmente_bloqueado():
            raise OperacionImposibleException("La cuenta está bloqueada temporalmente.")
        self.verificar_limite_transacciones()
        if monto < 0:
            raise ValueError("Es imposible depositar un valor negativo.")
        
        self._balance += monto
        deposito = self.transacciones(type="Depósito", monto= monto, cuenta_de_origen=self, cuenta_de_destino= None, descripcion=f"Depósito de: ${monto}")
        self.transacciones.append(deposito)

    def transferir(self, monto: float, cuenta_destino: "CuentaBancaria") -> float:
        try:
            self.retirar(monto)
        except SaldoInsuficienteException as ex:
            self.__transferencias_sin_saldo += 1
            print("Transferencia inválida", ex)
            return self.conseguir_balance()
        
        cuenta_destino.deposito(monto)
        self.transferir = self.transacciones(type="Transferencia", monto=monto, cuenta_de_origen=self, cuenta_de_destino=cuenta_destino, descripcion=f"Transferencia de ${monto} a la cuenta: {cuenta_destino}")
        self.transacciones.append(self.transferir)
        return self._balance

    def mostrar_historial(self):
        for x in self.transacciones:
            print(x)

    def __str__(self) -> str:
        return (f"Número de cuenta: {self.numero_de_cuenta}\n"
                f"Número de banco: {self.numero_bancario}\n"
                f"DNI: {self.cliente.dni}\n"
                f"Nombre del cliente: {self.cliente.nombre}\n"
                f"Saldo: {self._balance}")
    
    def esta_bloqueada_temporalmente(self):
        if self.bloqueada_hasta is not None and datetime.now() >= self.bloqueada_hasta:
            self.bloqueada_hasta = None
            self.cuenta_activa = True
            return False
        return self.bloqueada_hasta is not None

    def to_dict(self):
        return {
            "tipo_de_cuenta": type(self).__name__,
            "numero_bancario": self.numero_bancario,
            "numero_de_cuenta": self.numero_de_cuenta,
            "dni_del_cliente": self.cliente.dni,
            "saldo": self._balance,
            "tasa_de_interes": self.tasa_de_interes,
            "limite_de_sobregiro": self.limite_de_sobregiro,
            "cuenta_activa": self.cuenta_activa,
            "valor_de_comision": self.commission_value,
            "fecha_de_creacion": self.creation_date.isoformat(),
            "bloqueado_hasta": self.bloqueada_hasta.isoformat() if self.bloqueada_hasta else None,
            "transacciones": [t.to_dict() for t in self.transacciones],
            "tarjetas": [c.to_dict() for c in self.tarjetas]
        }