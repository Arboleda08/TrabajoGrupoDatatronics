from Servicios.Banco import Banco
from Modelos.Cuentas.CuentaBancaria import CuentaBancaria
from Modelos.Cuentas.card import Card

class AdministrarTarjetas:
    def __init__(self, banco: "Banco"):
        self.banco = banco

    def crear_tarjeta(self, cuenta: CuentaBancaria, pin: str, credito: bool, debito: bool):
          tarjeta = Card(cuenta, pin, credito, debito)
          cuenta.tarjetas.append(tarjeta)
          return tarjeta
  
    def bloquear_tarjeta(self, tarjeta):
        tarjeta.esta_bloqueada = True
  
    def desbloquear_tarjeta(self, tarjeta):
        tarjeta.esta_bloqueada = False
  
    def validar_tarjeta(self, tarjeta: "Card"):
          if tarjeta.esta_bloqueada:
              return False
          elif tarjeta.esta_expirado():
              return False
          else: 
              return True
          
    def cambiar_pin_tarjeta(self, tarjeta: "Card", actual_pin: str, nueva_pin: str):
        tarjeta.establecer_pin(actual_pin, nueva_pin)
          

  