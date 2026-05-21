from Modelos.Cuentas.CuentaBancaria import CuentaBancaria
from Modelos.Cuentas.Cliente import Cliente
from Modelos.Excepciones.OperacionImposibleException import OperacionImposibleException

class CuentaJuvenil(CuentaBancaria):
    def __init__(self, bank_number: int, client: Cliente, account_number: int | None = None):
        if not (13<= client.age <=20):
            raise OperacionImposibleException("Sólo clientes entre 13 y 20 años pueden tener una cuenta juvenil.")
        
        super().__init__(bank_number, client, account_number)
        self.daily_withdrawal_limit = 5
    
    def can_withdraw(self, amount):
        return (
            len(self.daily_withdraws()) < self.daily_withdrawal_limit
            and self._balance - amount >= 0
        )    
