import json
from datetime import datetime, timedelta
from Modelos.Cuentas.CuentaBancaria import CuentaBancaria
from Modelos.Cuentas.Cliente import Cliente
from DataBank.Modelos.Cuentas.transaccion import Transaction
from Modelos.Roles.Empleado import Empleado
from Modelos.Excepciones.OperacionImposibleException import OperacionImposibleException
from Modelos.Log.Log import Log
from Servicios.BonusAdmin import BonusAdmin
from DataBank.Servicios.analizar import Analize
from DataBank.Servicios.autentificar_objetos import AutenticateObjects
from DataBank.Servicios.enumerar_objetos import ListObjects
from DataBank.Servicios.administrar_cuentas import ManageAccounts
from DataBank.Servicios.administrar_creditos import ManageCredits
from DataBank.Servicios.administrar_empleados import ManageEmployees
from DataBank.Servicios.administrar_tarjetas import ManageCards
from DataBank.Servicios.notificar import Notificate
from DataBank.Servicios.reporte import ReportObjects
from DataBank.Servicios.buscar_objetos import SearchObjects

class Banco:
    def __init__(self, nombre: str, numero: int, clientes: list[Cliente], empleados: list[Empleado], global_transactiones: list[Transaction], registros: list[Log], bonus_admin: BonusAdmin):
        self.name = nombre
        self.bank_number = numero
        self.clients = clientes
        self.employees = empleados
        self.accounts: list[CuentaBancaria] = []
        self.global_transactions = global_transactiones
        self.registros = registros
        self.bonus_admin = bonus_admin
        self.tasa_de_interes = 0.6

        self.analizar = Analize(self)
        self.autentificar = AutenticateObjects(self)
        self.lista_objetos = ListObjects(self)
        self.administrar_cuentas = ManageAccounts(self)
        self.administrar_creditos = ManageCredits(self)
        self.administrar_empleados = ManageEmployees(self)
        self.administrar_tarjetas = ManageCards(self)
        self.notificar = Notificate(self)
        self.reportar = ReportObjects(self)
        self.buscar = SearchObjects(self)

    def validar_permiso(self, empleado: "Empleado", accion: str):
        permissions = {
            "Crear_empleado": empleado.puede_crear_usuario(),
            "Eliminar_empleado": empleado.puede_eliminar_usuario(),
            "Ver_informacion": empleado.puede_ver_informacion(),
            "Ver_reportes": empleado.puede_ver_reportes(),
            "Cambiar_rol": empleado.puede_cambiar_rol()
        }

        if accion not in permissions:
            raise OperacionImposibleException("Operación inválida")
        
        if not permissions[accion]:
            raise PermissionError(
                f"{empleado.nombre} no tiene permiso para {accion}"
            )
        
        return True

    def crear_cliente(self, empleado: "Empleado", datos_cliente: dict):
        self.validar_permiso(empleado, "Crear_empleado")

        client = Cliente (
            datos_cliente["nombre"],
            datos_cliente["dni"],
            datos_cliente["edad"],
            datos_cliente["profesion"]
        )

        self.clientes.append(client)
        return Cliente

    def cliente_actualización(self, empleado: "Empleado", cliente: "Cliente", tipo_cuenta: str):
        self.validar_permiso(empleado, "Crear_empleado")

        return self.gestion_cuentas.crear_cuenta(empleado, cliente, tipo_cuenta)


    def registrar_transaccion (self, transaccion: "Transaction"):
        self.global_transacciones.append(transaccion)

    def conseguir_historial_cuenta(self, cuenta: CuentaBancaria):
        return cuenta.transacciones

    def conseguir_historial_cliente(self, cliente: "Cliente"):
        transacciones = []

        for cuenta in self.cuentas:
            if cuenta.cliente == cliente:
                for transaction in cuenta.transacciones:
                    transacciones.append(transaction)

        return transacciones

    def conseguir_global_transacciones(self, empleado: "Empleado"):
        self.validar_permiso(empleado, "Ver_informacion")
        return self.global_transacciones

    def registrar_global_bonus(self):
        for empleado in self.empleado:
            self.bonus_admin.register(empleado)

    def conseguir_total_bonus(self):
        return self.bonus_admin.conseguir_total_bonus()

    def ordenar_cuentas_por_número(self):
        self.cuentas.sort(key=lambda cuenta: cuenta.número_de_cuenta)

        return self.cuentas

    def ordenar_cuentas_por_saldo(self):
        self.cuentas.sort(key=lambda cuenta: cuenta.conseguir_balance())

        return self.cuentas

    def registrar_registro(self, accion: str, empleado: "Empleado", estatus: bool, detalles: str):
        log = Log(empleado, accion, estatus, detalles)
        self.registros.append(log)
        
        return log

    def conseguir_registros(self):
        return self.registrar

    def cuentas_de_exportación_json(self):
        data = []

        for cuenta in self.cuentas:
            data.append({
                "Número de cuenta": cuenta.número_de_cuenta,
                "Número de banco": cuenta.numero_bancario,
                "Cliente": cuenta.cliente.nombre,
                "Saldo": cuenta.conseguir_balance()
            })
        with open("cuentas.json", "w") as file:
            json.dump(
                data,
                file,
                indent=4
            )
      
    def validar_límite_de_transferencia(self, monto: float, limite: float):
        if monto <= 0:
            raise ValueError("El monto debe ser mayor a 0.")
        return monto <= limite
          
  
    def bloqueo_temporal_de_cuenta(self, cuenta: "CuentaBancaria", minutos: int):
        if minutos <= 0:
            raise ValueError("Los minutos deben ser mayor a 0.")
        cuenta.cuenta_activa = False
        cuenta.bloqueada_hasta = datetime.now() + timedelta(minutes=minutos)
        return cuenta.bloqueada_hasta
  

    def listanegra_cliente(self, empleado: "Empleado", cliente: "Cliente", razon: str):
        self.validar_permiso(empleado, "Eliminar_empleado")
        if not hasattr(cliente, "esta_en_lista_negra"):
            cliente.esta_en_lista_negra = False
        cliente.esta_en_lista_negra = True
        cliente.motivo_lista_negra = razon
        self.registrar_log("Cliente en lista negra", empleado, True, f"Cliente {cliente.nombre} (DNI: {cliente.dni}) bloqueado. Motivo: {razon}")
        return True
    
    def exportar_data_json(self):
        data = {
            "nombre_banco": self.nombre,
            "numero_banco": self.numero_banco,
            "tasa_interes": self.tasa_interes,
            "clientes": [cliente.to_dict() for cliente in self.clientes],
            "empleados": [empleado.to_dict() for empleado in self.empleados],
            "cuentas": [cuenta.to_dict() for cuenta in self.cuentas],
            "transacciones": [transaccion.to_dict() for transaccion in self.transacciones],
            "registros": [registro.to_dict() for registro in self.registros]
        }

        with open(f"{self.nombre}_data.json", "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False) #aquí el ensure_ascii=False hace que caracteres como ñ o los acentos se guarden, al igual que encoding="utf-8". Recuerden el próximos usos.

        return True
    
##falta import_data_json
    
