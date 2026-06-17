from Servicios.Banco import Banco
from Modelos.Roles.EmpleadoAutenticable import EmpleadoAutenticable
from Modelos.Roles.Empleado import Empleado

class AutentificarObjetos:
    def __init__(self, banco: "Banco"):
        self.banco = banco
    
    def autenticar_usuario(self, empleado: "EmpleadoAutenticable", contraseña: str):
        if empleado.autenticar_usuario(contraseña):
            return True

        self.intento_de_verificación_fallido(empleado)
        return False
    
    def intento_de_verificación_fallido(self, empleado: "Empleado"):
        empleado.intentos_fallidos +=1

        if empleado.intentos_fallidos >= 3:
            self.bloquear_empleado(empleado)

    def bloquear_empleado(self, empleado: "Empleado"):
        empleado.esta_bloqueado= True


    def desbloquear_empleado(self, empleado: "Empleado"):
        empleado.esta_bloqueado = False
        empleado.intentos_fallidos = 0

        def detección_de_inicio_de_sesión_sospechoso(self):
          if self.historial_de_inicio_de_sesión_de_empleado() > 3:
              return True
          elif self.intentos_de_contraseña() > 3:
              return True
          elif self.ubicacion_inusual_de_inicio_de_sesion():
              return True
          elif self.historial_de_cambios_de_contraseña() > 3:
              return True
          elif self.contraseña != self.contraseña:
              return True