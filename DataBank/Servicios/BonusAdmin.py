from Modelos.Roles.Empleado import Empleado
class BonusAdmin:
    def __init__(self) -> None:
        self.__total_bonus: float = 0.0

    def registrar(self, empleado: Empleado):
        self.__total_bonus += empleado.obtener_bonus()

    def conseguir_total_bonus(self):
        return self.__total_bonus