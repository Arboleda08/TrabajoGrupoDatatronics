from Modelos.Cuentas.CuentaBancaria import CuentaBancaria
from Modelos.Cuentas.Cliente import Cliente

class CuentaEmpresarial(CuentaBancaria):
    def __init__(self, bank_number: int, client: Cliente, nit: int, authorized_users: list["Cliente"], account_number: int | None = None):
        super().__init__(bank_number, client, account_number)
        self.nit = nit
        self.authorized_users = authorized_users
        self.overdraft_limit = -10000
        self.daily_withdrawal_limit = 100
    
    def add_authorized_user(self, new_user: "Cliente"):
        self.authorized_users.append(new_user)
    
    def get_max_transactions_per_minute(self):
        return 10
    
    def can_withdraw(self, amount):
        return (
            len(self.daily_withdraws()) < self.daily_withdrawal_limit
            and self._balance - amount >= 0
        )    

