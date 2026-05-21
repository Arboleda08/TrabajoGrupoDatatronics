from Modelos.Roles.Empleado import Empleado
from Modelos.AutenticableHelper.AutenticableHelper import AutenticableHelper

class EmpleadoAutenticable(Empleado):
    def __init__(self, name: str, dni: int, position: str, salary: float, experience: int, password: str):
        super().__init__(name, dni, position, salary, experience)
        self._helper = AutenticableHelper()
        self.password = password

    def authenticate_user(self, new_password: str):
        return self._helper.comparate_passwords(self.password, new_password)

    def obtain_bonus(self) -> float:
        return 0