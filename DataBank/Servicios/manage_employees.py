from Servicios.Banco import Banco
from Modelos.Roles.EmpleadoAutenticable import EmpleadoAutenticable
from Modelos.Roles.Empleado import Empleado
from Modelos.Roles.Director import Director
from Modelos.Roles.Administrativo import Administrativo
from Modelos.Roles.Analista import Analista
from Modelos.Roles.Logistica import Logistica
from Modelos.Excepciones.OperacionImposibleException import OperacionImposibleException
class AdministrarEmpleados:
    def __init__(self, bank: "Banco"):
        self.bank = bank
    
    def add_employee(self, employee: "Empleado", target: "Empleado"):
        self.bank.validate_permission(employee, "Crear_empleado")
        self.bank.employees.append(target)
        return target

    def delete_employee(self, employee: "Empleado", target: "Empleado", new_role: str):
        self.bank.validate_permission(employee, "Eliminar_empleado")
        if target in self.bank.employees: 
            self.bank.employees.remove(target) 
            return True 
        return False

    def change_role(self, employee: "EmpleadoAutenticable", target: "EmpleadoAutenticable", new_role: str, department: str):
        self.bank.validate_permission(employee, "Crear_empleado")
  
        if new_role == "Analista":
            new_employee = Analista(target.name, target.get_dni(), target.experience, target.get_password())
        
        elif new_role == "Logistica":
            new_employee = Logistica(target.name, target.get_dni(), target.experience, target.get_password())
        
        elif new_role == "Administrativo":
            new_employee = Administrativo(target.name, target.get_dni(), target.experience, target.get_password())
        
        elif new_role == "Director":
            new_employee = Director(target.name, target.get_dni(), department, target.experience, target.get_password())
        
        else:
            raise OperacionImposibleException("Rol inválido.")

        self.bank.employees[self.bank.employees.index(target)] = new_employee
        return new_employee

    def approve_salary_increase(self, employee: "Empleado", target, amount: float):
        if not employee.can_modify_salary(target, amount):
            raise PermissionError("No es posible modificar el salario.")

        target.set_salary(target.get_salary() + amount)

        return target.get_salary()


    def apply_salary_increase(self, employee: "Empleado", target: "Empleado"):
        if not employee.can_raise_salary(target):
            raise PermissionError("No es posible aumentar el salario.")
        
        target.raise_salary()

        return target.get_salary()

    def evaluate_promotion(self, director: "Director", employee: "Empleado"):
        if not director.can_create_user():
            raise OperacionImposibleException("Permiso denegado.")
        
        if employee.can_request_promotion():
            return {
                "eligible": True,
                "reason": "El empleado cumple los requisitos mínimos para solicitar promoción."
            }
        
        return {
            "eligible": False,
            "reason": "El empleado no cumple todos los requisitos para ser promovido."
        }
    
    def approve_promotion(self, director: "Director", employee: "Empleado"):
        if not director.can_create_user():
            raise OperacionImposibleException("Permiso denegado.")

        employee.experience += 1

        return True
    
    def update_experience(self, employee: "Empleado", points: int):
        employee.experience += points

        return employee.experience
    

