from Modelos.Cuentas.CuentaBancaria import CuentaBancaria
import uuid
from datetime import datetime
class Transaction:
    def __init__(self, type: str, amount: float, origin_acc: "CuentaBancaria", destination_acc, description: str):
        self.id = uuid.uuid4().hex[:8]
        self.date = datetime.now()
        self.type = type
        self.amount = amount
        self.origin_account = origin_acc
        self.destination_account = destination_acc
        self.description = description

    def __str__(self) -> str:
        return (
            f"Id transacción: {self.id}\n"
            f"Fecha de la transacción: {self.date}\n"
            f"Tipo de la transacción: {self.type}\n"
            f"Monto de dinero: {self.amount}\n"
            f"Cuenta de destino: {self.destination_account}\n"
            f"Detalles y descripción: {self.description}\n"
            )