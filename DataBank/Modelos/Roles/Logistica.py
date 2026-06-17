from Modelos.Roles.EmpleadoAutenticable import EmpleadoAutenticable
class Logistica(EmpleadoAutenticable):
    def __init__(self, nombre: str, dni: int, experiencia: int, contraseña: str):
        super().__init__(nombre, dni, "Logística", 15000, experiencia, contraseña)

    def obtener_bonus(self):
        return self.conseguir_salario()* 0.3
    
    def porcentaje_incremento(self) -> float:
        return 0.02
    