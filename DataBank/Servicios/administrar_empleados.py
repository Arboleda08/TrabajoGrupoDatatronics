from Servicios.Banco import Banco
from Modelos.Roles.EmpleadoAutenticable import EmpleadoAutenticable
from Modelos.Roles.Empleado import Empleado
from Modelos.Roles.Director import Director
from Modelos.Roles.Administrativo import Administrativo
from Modelos.Roles.Analista import Analista
from Modelos.Roles.Logistica import Logistica
from Modelos.Excepciones.OperacionImposibleException import OperacionImposibleException
class AdministrarEmpleados:
    def __init__(self, banco "Banco"):
        self.banco = banco
    
    def añadir_empleado(self, empleado: "Empleado", objetivo: "Empleado"):
        self.banco.validar_permiso(empleado, "Crear_empleado")
        self.banco.empleado.append(objetivo)
        return objetivo

    def eliminar_empleado(self, empleado: "Empleado", objetivo: "Empleado", nuevo_role: str):
        self.banco.validar_permiso(empleado, "Eliminar_empleado")
        if objetivo in self.banco.empleado: 
            self.banco.empleado.remove(objetivo) 
            return True 
        return False

    def cambiar_role(self, empleado: "EmpleadoAutenticable", objetivo: "EmpleadoAutenticable", nuevo_role: str, departamento: str):
        self.banco.validar_permiso(empleado, "Crear_empleado")
  
        if nuevo_role == "Analista":
            nuevo_empleado = Analista(objetivo.nombre, objetivo.obtener_dni(), objetivo.experiencia, objetivo.obtener_contraseña())
        
        elif nuevo_role == "Logistica":
            nuevo_empleado = Logistica(objetivo.nombre, objetivo.obtener_dni(), objetivo.experiencia, objetivo.obtener_contraseña())
        
        elif nuevo_role == "Administrativo":
            nuevo_empleado = Administrativo(objetivo.objetivo, objetivo.obtener_dni(), objetivo.experiencia, objetivo.obtener_contraseña())
        
        elif nuevo_role == "Director":
            nuevo_empleado = Director(objetivo.nombre, objetivo.obtener_dni(), departamento, objetivo.experiencia, objetivo.obtener_contraseña())
        
        else:
            raise OperacionImposibleException("Rol inválido.")

        self.banco.empleados[self.banco.empleados.index(objetivo)] = nuevo_empleado
        return nuevo_empleado

    def aprobar_incremento_salario(self, empleado: "Empleado", objetivo, monto: float):
        if not empleado.puede_modificar_salario(objetivo, monto):
            raise PermissionError("No es posible modificar el salario.")

        objetivo.establecer_salaro(objetivo.obtener_salario() + monto)

        return objetivo.obtener_salario()


    def aplicar_incremento_salario(self, empleado: "Empleado", objetivo: "Empleado"):
        if not empleado.puede_aumentar_salario(objetivo):
            raise PermissionError("No es posible aumentar el salario.")
        
        objetivo.aumentar_salario()

        return objetivo.obtener_salario()

    def evaluar_promocion(self, director: "Director", empleado: "Empleado"):
        if not director.can_create_user():
            raise OperacionImposibleException("Permiso denegado.")
        
        if empleado.puede_pedir_promocion():
            return {
                "eligible": True,
                "razon": "El empleado cumple los requisitos mínimos para solicitar promoción."
            }
        
        return {
            "eligible": False,
            "razon": "El empleado no cumple todos los requisitos para ser promovido."
        }
    
    def aprobar_promocion(self, director: "Director", empleado: "Empleado"):
        if not director.puede_crear_usuario():
            raise OperacionImposibleException("Permiso denegado.")

        empleado.experiencia += 1

        return True
    
    def actualizar_experiencia(self, empleado: "Empleado", puntos: int):
        empleado.experiencia += puntos

        return empleado.experiencia
    

