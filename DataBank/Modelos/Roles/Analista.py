from Modelos.Roles.AutentificarEmpleado import AutentificarEmpleado
class Analista(AutentificarEmpleado):
    def __init__(self, nombre: str, dni: int, experiencia: int, contraseña: str):
        super().__init__(nombre, dni, "Analista", 30000, experiencia, contraseña)
    
    def obtener_bonus(self):
        return self.conseguir_salario() * 0.2
    
    def puede_ver_reportes(self) -> bool:
        return True
    
    def porcentaje_de_incremento(self) -> float:
        return 0.08
