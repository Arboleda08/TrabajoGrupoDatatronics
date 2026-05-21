from Modelos.Roles.EmpleadoAutenticable import EmpleadoAutenticable
class Administrativo(EmpleadoAutenticable):
    def __init__(self, name: str, dni: int, experience: int, password: str):
        super().__init__(name, dni, "Administrativo", 20000, experience, password)

    def obtain_bonus(self):
        return self.get_salary() * 0.15
    
    def can_see_reports(self) ->bool:
        return True
    
    def can_see_information(self) -> bool:
        return True
    
    def can_create_user(self) -> bool:
        return True
    
    def can_delete_user(self) ->bool:
        return True
    
    def percentage_increase(self) -> float:
        return 0.08
    

    