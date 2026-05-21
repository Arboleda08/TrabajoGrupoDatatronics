from Modelos.Roles.EmpleadoAutenticable import EmpleadoAutenticable
class Analista(EmpleadoAutenticable):
    def __init__(self, name: str, dni: int, experience: int, password: str):
        super().__init__(name, dni, "Analista", 30000, experience, password)
    
    def obtain_bonus(self):
        return self.get_salary() * 0.2
    
    def can_see_reports(self) -> bool:
        return True
    
    def percentage_increase(self) -> float:
        return 0.08