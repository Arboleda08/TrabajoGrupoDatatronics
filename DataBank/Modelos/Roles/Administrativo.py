from Modelos.Roles.AutentificarEmpleado import AutentificarEmpleado
class Administrativo(AutentficarEmpleado):
    def __init__(self, name: str, dni: int, experience: int, password: str):
        super().__init__(nombre, dni, "Administrativo", 20000, experiencia, contraseña)

    def obtener_bonus(self):
        return self.get_salary() * 0.15
    
    def puede_ver_reportes(self) ->bool:
        return True
    
    def puede_ver_informacion(self) -> bool:
        return True
    
    def puede_crear_usuarios(self) -> bool:
        return True
    
    def puede_eliminar_usuarios(self) ->bool:
        return True
    
    def porcentaje_de_aumento(self) -> float:
        return 0.08
    

    
