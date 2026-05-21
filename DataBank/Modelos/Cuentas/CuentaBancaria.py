from .Cliente import Cliente
from Modelos.Cuentas.Transaccion import Transaction
from Modelos.Excepciones.SaldoInsuficienteException import SaldoInsuficienteException
from Modelos.Excepciones.OperacionImposibleException import OperacionImposibleException
import uuid
from datetime import datetime
from datetime import timedelta

class CuentaBancaria:
    account_count: int = 0

    def __init__(self, bank_number: int, client: Cliente, account_number: int | None = None):
        if bank_number is None or bank_number <= 0:
            raise ValueError("Es obligatorio un número de agencia válido")
        if account_number is not None and account_number <= 0:
            raise ValueError("Es obligatorio ingresar el número de cuenta")

        self.bank_number = bank_number
        self.account_number = (
            account_number if account_number is not None
            else str(uuid.uuid4())[:8]
        )
        self.client = client
        self._balance: float = 0.0
        self.interest_rate: float = 0.0
        self.overdraft_limit: float = 0.0
        self.account_active: bool = False
        self.commission_value: float = 0.0
        self.__withdrawals_without_balance: int = 0
        self.__transfers_without_balance: int = 0
        self.transactions: list["Transaction"] = []
        self.max_transactions_per_minute = 1
        self.creation_date = datetime.now()

        CuentaBancaria.account_count += 1

    def get_balance(self) -> float:
        return self._balance

    def get_withdrawals_without_balance(self) -> int:
        return self.__withdrawals_without_balance

    def get_transfers_without_balance(self) -> int:
        return self.__transfers_without_balance
    
    def get_min_balance(self)-> float:
        return 0

    def get_max_transactions_per_minute(self):
        return self.max_transactions_per_minute
    
    def can_withdraw(self, amount: float)-> bool:
        if self._balance - amount < self.get_min_balance():
            return False
        return True
    
    def daily_withdraws(self):
        today = datetime.now().date()
        return [
        t for t in self.transactions
        if t.type == "Retiro" and t.date.date() == today
        ]
    
    def check_transaction_limit(self):
        now = datetime.now()
        one_minute_ago = now - timedelta(minutes=1)

        recent = [
            t for t in self.transactions
            if t.date >= one_minute_ago
        ]

        if len(recent) >= self.get_max_transactions_per_minute():
            raise OperacionImposibleException("Límite excedido")

    def withdraw(self, amount: float) -> bool:
        self.check_transaction_limit()
        
        if amount <= 0:
            raise ValueError("Monto inválido")

        if not self.can_withdraw(amount):
            self.__withdrawals_without_balance += 1
            raise SaldoInsuficienteException("No puede superar el límite de la cuenta")

        self._balance -= amount
        withdraw = Transaction(type="Retiro", amount= amount, origin_acc=self, destination_acc= None, description=f"Retiro de: ${amount}")
        self.transactions.append(withdraw)
        return True

    def deposit(self, amount: float) -> None:
        self.check_transaction_limit()
        if amount < 0:
            raise ValueError("Es imposible depositar un valor negativo.")
        
        self._balance += amount
        deposit = Transaction(type="Depósito", amount= amount, origin_acc=self, destination_acc= None, description=f"Depósito de: ${amount}")
        self.transactions.append(deposit)

    def transfer(self, amount: float, target_account: "CuentaBancaria") -> float:
        try:
            self.withdraw(amount)
        except SaldoInsuficienteException as ex:
            self.__transfers_without_balance += 1
            print("Transferencia inválida", ex)
        target_account.deposit(amount)

        transfer = Transaction(type="Transferencia", amount=amount, origin_acc= self, destination_acc= target_account, description=f"Transferencia de ${amount} a la cuenta: {target_account}")
        self.transactions.append(transfer)
        return self._balance

    def show_history(self):
        for x in self.transactions:
            print(x)

    def __str__(self) -> str:
        return (f"Número de cuenta: {self.account_number}\n"
                f"Número de banco: {self.bank_number}\n"
                f"DNI: {self.client.dni}\n"
                f"Nombre del cliente: {self.client.name}\n"
                f"Saldo: {self._balance}")