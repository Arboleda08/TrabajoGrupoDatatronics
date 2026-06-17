from Modelos.Cuentas.CuentaBancaria import CuentaBancaria
from Modelos.Cuentas.Cliente import Cliente

class CuentaEmpresarial(CuentaBancaria):
    def __init__(self, numero_bancario: int, cliente: Cliente, nit: int, usuarios_autorizados: list["Cliente"], numero_de_cuenta: int | None = None):
        super().__init__(numero_bancario, cliente, numero_de_cuenta)
        self.nit = nit
        self.usuarios_autorizados = usuarios_autorizados
        self.limite_de_sobregiro = -10000
        self.limite_diario_retiros = 100
    
    def añadir_usuario_autorizado(self, nuevo_usuario: "Cliente"):
        self.usuarios_autorizados.append(nuevo_usuario)
    
    def obtener_maximo_transacciones_por_minuto(self):
        return 10
    
    def puede_retirar(self, monto: float):
        return (
            len(self.retiros_diarios()) < self.limite_diario_retiros
            and self._balance - monto >= 0
        )    
    
    def to_dict(self):
        data = super().to_dict()
        data["nit"] = self.nit
        data["limite_diario_retiros"] = self.limite_diario_retiros
        data["usuarios_autorizados"] = [user.dni for user in self.usuarios_autorizados]
        return data

