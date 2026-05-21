from Modelos.Roles.Empleado import Empleado
class BonusAdmin:
    def __init__(self) -> None:
        self.__total_bonus: float = 0.0

    def register(self, employee: Empleado):
        self.__total_bonus += employee.obtain_bonus()

    def get_total_bonus(self):
        return self.__total_bonus