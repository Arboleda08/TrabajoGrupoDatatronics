from Modelos.Cuentas.CuentaBancaria import CuentaBancaria
from Modelos.Cuentas.Cliente import Cliente
from Modelos.Excepciones.OperacionImposibleException import OperacionImposibleException

class CuentaJuvenil(CuentaBancaria):
    def __init__(self, numero_bancario: int, cliente: Cliente, numero_de_cuenta: int | None = None):
        if not (13<= cliente.age <=20):
            raise OperacionImposibleException("Sólo clientes entre 13 y 20 años pueden tener una cuenta juvenil.")
        
        super().__init__(numero_bancario, cliente, numero_de_cuenta)
        self.limite_diario_retiros = 5
    
    def puede_retirar(self, monto):
        return (
            len(self.retiros_diarios()) < self.limite_diario_retiros
            and self._balance - monto >= 0
        )    
    
    def to_dict(self):
        data = super().to_dict()
        data["limite_diario_retiros"] = self.limite_diario_retiros
        return data
