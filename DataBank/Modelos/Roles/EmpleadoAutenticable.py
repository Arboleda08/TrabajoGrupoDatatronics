from datetime import datetime
from Modelos.Roles.Empleado import Empleado
from Modelos.AutenticableHelper.AutenticableHelper import AutenticableHelper

class EmpleadoAutenticable(Empleado):
    def __init__(self, nombre: str, dni: int, posicion: str, salario: float, experiencia: int, password: str):
        super().__init__(nombre, dni, posicion, salario, experiencia)
        self._helper = AutenticableHelper()
        self.__contraseña = password
        self.bloqueado_hasta = None

    def conseguir_contraseña(self):
        return self.__contraseña
    
    def autenticar_usuario(self, nueva_contraseña: str):
        return self._helper.comparate_passwords(self.conseguir_contraseña(), nueva_contraseña)

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