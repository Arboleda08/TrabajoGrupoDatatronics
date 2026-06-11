from Modelos.Roles.AutentificarEmpleado import AutentificarEmpleado 
class Logistica(AutentificarEmpleado):
    def __init__(self, nombre: str, dni: int, experiencia: int, contraseña: str):
        super().__init__(nombre, dni, "Logística", 15000, experiencia, contraseña)

    def obtener_bonus(self):
        return self.conseguir_salario()* 0.3
    
    def porcentaj_incrementado(self) -> float:
        return 0.02
