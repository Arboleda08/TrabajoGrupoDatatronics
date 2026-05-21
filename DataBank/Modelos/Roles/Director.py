from Modelos.Roles.EmpleadoAutenticable import EmpleadoAutenticable
from Modelos.Roles.Empleado import Empleado
class Director(EmpleadoAutenticable):
    def __init__(self, name: str, dni: int, department: str, experience: int, password: str):
        super().__init__(name, dni, "Director", 50000, experience, password)
        self.department = department

    def obtain_bonus(self):
        return self.get_salary() * 0.5

    def can_approve_credit(self, amount: float)-> bool:
        return amount <= 100000
    
    def can_modify_salary(self, employee: "Empleado", amount: float)-> bool:
        return amount <= 0.2 * employee.get_salary()
    
    def can_see_reports(self) ->bool:
        return True
    
    def can_see_information(self) -> bool:
        return True
    
    def can_approve_transfer(self, amount: float) -> bool:
        return amount <= 50000
    
    def can_create_user(self) -> bool:
        return True
    
    def can_delete_user(self) ->bool:
        return True
    
    def can_raise_salary(self, employee: "Empleado") -> bool:
        return True
    
    def percentage_increase(self) -> float:
        return 0.06
    