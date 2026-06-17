from Modelos.Roles.EmpleadoAutenticable import EmpleadoAutenticable
from Modelos.Roles.Empleado import Empleado
class Director(EmpleadoAutenticable):
    def __init__(self, nombre: str, dni: int, departamento: str, experiencia: int, contraseña: str):
        super().__init__(nombre, dni, "Director", 50000, experiencia, contraseña)
        self.departamento = departamento
        self.puede_cambiar_rol = True

    def obtener_bonus(self):
        return self.conseguir_salario() * 0.5

    def puede_aprobar_credito(self, monto: float)-> bool:
        return monto <= 100000
    
    def puede_modificar_salario(self, empleado: "Empleado", monto: float)-> bool:
        return monto <= 0.2 * empleado.get_salary()
    
    def puede_ver_reportes(self) ->bool:
        return True
    
    def puede_ver_informacion(self) -> bool:
        return True
    
    def puede_aprobar_transferencia(self, monto: float) -> bool:
        return monto <= 50000
    
    def puede_crear_usuario(self) -> bool:
        return True
    
    def puede_eliminar_usuario(self) ->bool:
        return True
    
    def puede_aumentar_salario(self, empleado: "Empleado") -> bool:
        return True
    
    def porcentaje_aumento(self) -> float:
        return 0.06
    
    def to_dict(self):
        data = super().to_dict()
        data["departamento"] = self.departamento
        return data