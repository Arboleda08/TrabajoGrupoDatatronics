from Modelos.Cuentas.CuentaBancaria import CuentaBancaria
from Modelos.Excepciones.OperacionImposibleException import OperacionImposibleException
from Modelos.Cuentas.Cliente import Cliente

class CuentaCorriente(CuentaBancaria):
    def __init__(self, bank_number: int, client: Cliente, account_number: int | None = None):
        super().__init__(bank_number, client, account_number)
        self.overdraft_limit = -500
    
    def get_min_balance(self):
        return self.overdraft_limit
    
    def withdraw(self, amount: float) -> bool:
        if amount <=0:
            raise OperacionImposibleException("Monto Inválido")
        
        if self.get_balance() - amount < self.overdraft_limit:
            raise OperacionImposibleException("Límite de sobregiro excedido")
        
        return super().withdraw(amount)
    
    def get_max_transactions_per_minute(self):
        return 2
    
    def can_withdraw(self, amount):
        return self._balance - amount >= self.get_min_balance()