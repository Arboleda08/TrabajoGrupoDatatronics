import uuid
from Modelos.Roles.Empleado import Empleado
from datetime import datetime

class Log:
    def __init__(self, empleado: Empleado, accion: str, estado: str, detalle: str = ""):
        self.id = uuid.uuid4().hex[:8]
        self.fecha = datetime.now()

        self.empleado = empleado
        self.accion = accion
        self.estado = estado   
        self.detalle = detalle