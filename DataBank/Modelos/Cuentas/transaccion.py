from Modelos.Cuentas.CuentaBancaria import CuentaBancaria
import uuid
from datetime import datetime
class Transaccion:
    def __init__(self, tipo: str, monto: float, cuenta_de_origen: "CuentaBancaria", cuenta_de_destino, descripcion: str):
        self.id = uuid.uuid4().hex[:8]
        self.fecha = datetime.now()
        self.tipo = tipo
        self.monto = monto
        self.cuenta_de_origen = cuenta_de_origen
        self.cuenta_de_destino = cuenta_de_destino
        self.descripcion = descripcion

    def __str__(self) -> str:
        return (
            f"Id transacción: {self.id}\n"
            f"Fecha de la transacción: {self.fecha}\n"
            f"Tipo de la transacción: {self.tipo}\n"
            f"Monto de dinero: {self.monto}\n"
            f"Cuenta de destino: {self.cuenta_de_destino}\n"
            f"Detalles y descripción: {self.descripcion}\n"
            )
    
    def to_dict(self):
        return {
            "id": self.id,
            "fecha": self.fecha.isoformat(),
            "tipo": self.tipo,
            "monto": self.monto,
            "cuenta_de_origen": self.cuenta_de_origen.account_number,
            "cuenta_de_destino": self.cuenta_de_destino.account_number if self.cuenta_de_destino else None,
            "descripcion": self.descripcion
        }