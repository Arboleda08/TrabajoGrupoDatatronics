class Empleado:
    total_empleados: int = 0
    
    def __init__(self, nombre: str, dni: int, posicion: str, salario: float, experiencia: int) -> None:
        Empleado.total_empleados +=1
        self.nombre = nombre
        self.__posicion = posicion
        self.__dni = dni
        self.__salario = salario
        self.experiencia = experiencia
        self.esta_bloqueado = False
        self.intentos_fallidos = 0
        self.puede_cambiar_role = False
        self.bloqueado_hasta = None

    def conseguir_posicion(self):
        return (self.__posicion)
    
    def establecer_posicion(self, nueva_posicion):
        self.__posicion = nueva_posicion

    def conseguir_dni(self):
        return (self.__dni)
    
    def conseguir_salario(self):
        return (self.__salario)
    
    def establecer_salario(self, nuevo_salario):
        self.__salario = nuevo_salario
    
    def obtener_bonus(self) -> float:
        raise NotImplementedError("El método debe ser implementado en la sublclase.")

    def aumentar_salario(self):
        self.establecer_salario(
            self.conseguir_salario() * (1 + self.porcentaje_de_incremento())
        )
    
    def puede_aprobar_creditos(self, monto: float)-> bool:
        return False
    
    def puede_modificar_salario(self, empleado: "Empleado", monto: float)-> bool:
        return False
    
    def puede_ver_reportes(self) ->bool:
        return False
    
    def puede_ver_informacion(self) -> bool:
        return False
    
    def puede_aprobar_transferencia(self, monto: float) -> bool:
        return False
    
    def puede_crear_usuario(self) -> bool:
        return False
    
    def puede_eliminar_usuario(self) ->bool:
        return False
    
    def puede_aumentar_salario(self, empleado: "Empleado") -> bool:
        return False
    
    def porcentaje_incrementado(self) -> float:
        return 0.01
    
    def puede_solicitar_promocion(self):
        return self.experience >= 5
    def to_dict(self):
        return {
            "tipo_de_empleado": tipo(self).__nombre__,
            "nombre": self.name,
            "dni": self.establecer_dni(),
            "posicion": self.establecer_posicion(),
            "salario": self.establecer_salario(),
            "experiencia": self.experiencia,
            "esta_bloqueado": self.esta_bloqueado,
            "intentos_fallidos": self.intentos_fallidos,
            "puede_cambiar_roles": self.puede_cambiar_roles,
            "bloqueado_hasta": self.bloqueado_hasta.isoformato() if self.bloqueado_hasta else None
        }
  
