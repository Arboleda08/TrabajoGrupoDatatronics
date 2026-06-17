from Servicios.Banco import Banco

class Notificate:
    def __init__(self, bank: "Banco"):
        self.bank = bank

    def send_notification(self, notification_type: str, message: str):
        notification_types = ["client", "employee"]
        message = f"Notificación: {message}"
        if notification_type not in notification_types:
            raise ValueError("Tipo de notificación inválida")
        elif notification_type == "client":
            print(f"Notificación enviada al cliente: {message}")
        elif notification_type == "employee":
            print(f"Notificación enviada al empleado: {message}")

  
    def notify_account_blocked(self):
          self.send_notification("client", "Su trajeta ha sido bloqueada.")