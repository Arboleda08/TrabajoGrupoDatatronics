from Modelos.Cuentas.CuentaBancaria import CuentaBancaria
from Modelos.Excepciones.OperacionImposibleException import OperacionImposibleException
from Modelos.Cuentas.Cliente import Cliente

class CuentaAhorros(CuentaBancaria):
    def __init__(self, numerio_bancario: int, cliente: Cliente, nombre_cuenta: int | None = None):
        super().__init__(numerio_bancario, cliente, nombre_cuenta)
        self.tasa_interes = 0.5
        self.limite_diario_retiro = 6
        
    def aplicar_tasa_interes(self):
        self._balance += self._balance * self.tasa_interes

    def retiro(self, monto: float) -> bool:
        if monto <=0:
            raise OperacionImposibleException("Monto Inválido")
        
        if monto > self.conseguir_balance():
            raise OperacionImposibleException("La cuenta de ahorros no permite saldo negativo")
        
        return super().retiro(monto)
    
    def obtener_maximo_transacciones_por_minuto(self):
        return 2
    
    def puede_retirar(self, monto):
        return (
            len(self.retiros_diarios()) < self.limite_diario_retiro
            and self._balance - monto >= 0
        )    

    def to_dict(self):
        data = super().to_dict()
        data["limite_diario_retiro"] = self.limite_diario_retiro
        return data
