from Modelos.Cuentas.Cliente import Cliente

class Credito:
    def __init__(self, monto: float, tasa_interes: float, meses: int, cliente: Cliente):
        self.monto = monto
        self.tasa_interes = tasa_interes
        self.meses = meses
        self.cliente = cliente
        self.aprobado = False
        self.saldo_restante = monto
        self.estado = "Pendiente"
        cliente.añadir_credito(self)

    def __str__(self) -> str:
        return (f"Credito de {self.monto} para {self.cliente.nombre}")
    
    def to_dict(self):
        return {
            "monto": self.monto,
            "tasa_interes": self.tasa_interes,
            "meses": self.meses,
            "aprobado": self.aprobado,
            "saldo_restante": self.saldo_restante,
            "estado": self.estado
        }
