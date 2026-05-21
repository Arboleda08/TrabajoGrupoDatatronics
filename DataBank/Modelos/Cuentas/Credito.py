from Modelos.Cuentas.Cliente import Cliente

class Credito:
    def __init__(self, amount: float, interest_rate: float, months: int, client: Cliente):
        self.amount = amount
        self.interest_rate = interest_rate
        self.months = months
        self.client = client
        self.approved = False
        self.remaining_balance = amount
        self.status = "Pendiente de aprobación."
        client.add_credit(self)

    def __str__(self) -> str:
        return (f"Credito de {self.amount} para {self.client.name}")
