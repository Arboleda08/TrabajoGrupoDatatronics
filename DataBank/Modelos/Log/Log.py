import uuid
from Modelos.Roles.Empleado import Empleado
from datetime import datetime

class Registro:
    def __init__(self, empleado: Empleado, accion: str, estatus: bool, detalles: str = ""):
        self.id = uuid.uuid4().hex[:8]
        self.fecha = datetime.now()
        self.empleado = empleado
        self.accion = accion
        self.estatus = estatus
        self.detalles = detalles

    def to_dict(self):
        return {
            "id": self.id,
            "date": self.fecha.isoformat(),
            "employee_dni": self.empleado.get_dni(),
            "action": self.accion,
            "status": self.estatus,
            "details": self.detalles
        }