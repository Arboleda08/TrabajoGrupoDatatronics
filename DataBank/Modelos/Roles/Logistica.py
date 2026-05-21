from Modelos.Roles.EmpleadoAutenticable import EmpleadoAutenticable
class Logistica(EmpleadoAutenticable):
    def __init__(self, name: str, dni: int, experience: int, password: str):
        super().__init__(name, dni, "Logística", 15000, experience, password)

    def obtain_bonus(self):
        return self.get_salary()* 0.3
    
    def percentage_increase(self) -> float:
        return 0.02
    