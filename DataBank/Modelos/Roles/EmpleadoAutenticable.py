from datetime import datetime
from Modelos.Roles.Empleado import Empleado
from Modelos.AyudanteAuténtico.AyudanteAuténtico import AyudanteAuténtico

class AutentificarEmpleado(Empleado):
    def __init__(self, nombre: str, dni: int, posicion: str, salario: float, experiencio: int, contraseña: str):
        super().__init__(nombre, dni, posicion, salario, experiencia)
        self._ayudante = AyudanteAutentico()
        self.__contraseña = contraseña
        self.bloquear_hasta = None

    def conseguir_contraseña(self):
        return self.__contraseña
    
    def autentificar_usuario(self, nueva_contraseña: str):
        return self._ayudante.comparar_contraseñas(self.consegir_contraseña(), nueva_contraseña)

    def obtener_bonus(self) -> float:
        return 0
    
    def esta_bloqueado(self):
        if self.bloqueado_hasta is not None and datetime.now() >= self.bloqueado_hasta:
            self.bloqueado_hasta = None
            return False
        return self.bloqueado_hasta is not None
    
    def to_dict(self):
        data = super().to_dict()
        data["contraseña"] = self.conseguir_contraseña()
        return data
