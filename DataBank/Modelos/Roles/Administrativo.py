from Modelos.Roles.EmpleadoAutenticable import EmpleadoAutenticable
class Administrativo(EmpleadoAutenticable):
    def __init__(self, nombre: str, dni: int, experiencia: int, contraseña: str):
        super().__init__(nombre, dni, "Administrativo", 20000, experiencia, contraseña)

    def obtener_bonus(self):
        return self.conseguir_salario() * 0.15
    
    def puede_ver_reportes(self) ->bool:
        return True
    
    def puede_ver_informacion(self) -> bool:
        return True
    
    def puede_crear_usuario(self) -> bool:
        return True
    
    def puede_eliminar_usuario(self) ->bool:
        return True
    
    def porcentaje_aumento(self) -> float:
        return 0.08
    