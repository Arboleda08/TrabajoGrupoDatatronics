from Servicios.Banco import Banco
from Modelos.Cuentas.CuentaAhorros import CuentaAhorros
from Modelos.Cuentas.CuentaBancaria import CuentaBancaria
from Modelos.Cuentas.CuentaCorriente import CuentaCorriente
from Modelos.Cuentas.CuentaEmpresarial import CuentaEmpresarial
from Modelos.Cuentas.CuentaJuvenil import CuentaJuvenil
from Modelos.Cuentas.Cliente import Cliente
from Modelos.Roles.Empleado import Empleado
from Modelos.Excepciones.OperacionImposibleException import OperacionImposibleException

class AdministrarCuentas:
    def __init__(self, banco: "Banco"):
        self.banco = banco

    def crear_cuenta(self, empleado: "Empleado", cliente: "Cliente", tipo_cuenta: str):
        self.banco.validar_permiso(empleado, "Crear_cliente")

        tipo_cuenta = {
            "Ahorros": CuentaAhorros,
            "Corriente": CuentaCorriente,
            "Empresarial": CuentaEmpresarial,
            "Juvenil": CuentaJuvenil
        }

        if tipo_cuenta not in tipo_cuenta:
            raise ValueError("Tipo de cuenta inválido")

        clase_de_cuenta = tipo_cuenta[tipo_cuenta]

        cuenta = clase_de_cuenta(
            numero_bancario = self.banco.numero_bancario,
            cliente = cliente
        )

        self.banco.cuentas.append(cuenta)

        return cuenta

    def eliminar_cuenta(self, empleado: "Empleado", cuenta: CuentaBancaria):
        self.banco.validar_permiso(empleado, "Borrar_cuenta")

        if cuenta in self.banco.cuentas:
            self.banco.cuentas.remove(cuenta)
            return True

        return False

    def cambiar_estado_cuenta(self, empleado: "Empleado", cuenta: CuentaBancaria):
        self.banco.validar_permiso(empleado, "Borrar_cuenta")

        cuenta.cuenta_activa = not cuenta.cuenta_activa

        return cuenta.cuenta_activa

    def cerrar_cuenta(self, empleado: "Empleado", cuenta: "CuentaBancaria"):
        self.banco.validar_permiso(empleado, "Borrar_cuenta")
        if cuenta.conseguir_balance() != 0:
            raise OperacionImposibleException("No se puede cerrar una cuenta con saldo pendiente.")
        cuenta.cuenta_activa = False
        self.banco.cuentas.remover(cuenta)
        self.banco.registrar_registro("Cierre_de_cuenta", empleado, True, "Cierre de cuenta por no uso")
        return True
    
    def aplicar_tarifa_mensual(self, empleado: "Empleado", cuenta: "CuentaBancaria", tarifa: float):
        self.banco.validar_permiso(empleado, "Borrar_cuenta")
        if not cuenta.cuenta_activa:
            raise OperacionImposibleException("La cuenta no está activa.")
        if tarifa <= 0:
            raise ValueError("La comisión debe ser mayor a 0.")
        cuenta.retirar(tarifa)
        self.banco.registrar_registro("Cuota de manejo", empleado, True, "Cobro de cuota de manejo")
        return cuenta.conseguir_balance()