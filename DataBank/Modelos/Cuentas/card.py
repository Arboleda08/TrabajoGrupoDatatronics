import uuid
from datetime import datetime, timedelta
from Modelos.Cuentas.CuentaBancaria import CuentaBancaria

class Tarjeta:
    def __init__(self, cuenta: "CuentaBancaria", pin: str, tipo_credito: bool, tipo_debito: bool):
        if tipo_credito and tipo_debito:
            raise ValueError("Una tarjeta no puede ser débito y crédito al mismo tiempo.")
        if not tipo_credito and not tipo_debito:
            raise ValueError("Una tarjeta debe ser débito o crédito.")
    
        self.numero_tarjeta = uuid.uuid4().hex[:16].upper()
        self.__pin = pin
        self.esta_bloqueado = False
        self.expiration_date = datetime.now() + timedelta(days=365 * 4)
        self.cuenta = cuenta
        self.titular = cuenta.cliente
        self.es_tarjeta_de_credito = tipo_credito
        self.es_tarjeta_de_debito = tipo_debito

        if self.es_tarjeta_de_credito:
            self.tipo_tarjeta = "Crédito"
        elif self.es_tarjeta_de_debito:
            self.tipo_tarjeta = "Débito"

    def __str__(self):
        return(
            f"Nombre del titular: {self.titular.name}\n"
            f"Número de tarjeta: {self.numero_tarjeta}\n"
            f"Fecha de expiración: {self.fecha_expiracion}\n"
            f"Tipo de tarjeta: {self.tipo_tarjeta}\n"
            f"Cuenta bancaria asociada: {self.cuenta.numero_cuenta}\n"
        )
    
    def obtener_pin(self):
        return self.__pin
    
    def establecer_pin(self, pin_actual: str, nuevo_pin: str):
        if pin_actual == self.conseguir_pin():
            self.__pin = nuevo_pin
    
    def esta_vencida(self):
        return datetime.now() > self.fecha_expiracion
    
    def to_dict(self):
        return{
            "nombre_titular": self.titular.name,
            "numero_tarjeta": self.numero_tarjeta,
            "fecha_expiracion": self.fecha_expiracion.isoformat(),
            "numero_cuenta": self.cuenta.numero_cuenta,
            "tipo_tarjeta": self.tipo_tarjeta,
            "esta_bloqueada": self.esta_bloqueado
        }