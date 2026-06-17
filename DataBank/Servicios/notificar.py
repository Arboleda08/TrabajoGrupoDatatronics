from Servicios.Banco import Banco

class Notificate:
    def __init__(self, banco: "Banco"):
        self.banco = banco

    def enviar_notificacion(self, tipo_de_notificacion: str, mensaje: str):
        tipos_de_notificacion = ["cliente", "empleado"]
        mensaje = f"Notificación: {mensaje}"
        if tipo_de_notificacion not in tipos_de_notificacion:
            raise ValueError("Tipo de notificación inválida")
        elif tipo_de_notificacion == "client":
            print(f"Notificación enviada al cliente: {mensaje}")
        elif tipo_de_notificacion == "empleado":
            print(f"Notificación enviada al empleado: {mensaje}")

  
    def notificacion_cuenta_bloqueada(self):
          self.enviar_notificacion("cliente", "Su trajeta ha sido bloqueada.")