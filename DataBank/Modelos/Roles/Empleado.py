class Empleado:
    total_empleados: int = 0
    
    def __init__(self, nombre: str, dni: int, posicion: str, salario: float, experiencia: int) -> None:
        Empleado.total_empleados +=1
        self.nombre = nombre
        self.__position = posicion
        self.__dni = dni
        self.__salary = salario
        self.experiencia = experiencia
        self.esta_bloqueado = False
        self.intentos_fallidos = 0
        self.puede_cambiar_rol = False
        self.bloqueado_hasta = None

    def conseguir_posicion(self):
        return (self.__posicion)
    
    def establecer_posicion(self, nueva_posicion):
        self.__position = nueva_posicion

    def conseguir_dni(self):
        return (self.__dni)
    
    def conseguir_salario(self):
        return (self.__salary)
    
    def establecer_salario(self, nuevo_salario):
        self.__salary = nuevo_salario
    
    def obtener_bonus(self) -> float:
        raise NotImplementedError("El método debe ser implementado en la sublclase.")

    def aumentar_salario(self):
        self.establecer_salario(
            self.conseguir_salario() * (1 + self.porcentaje_aumento())
        )
    
    def puede_aprobar_credito(self, monto: float)-> bool:
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
    
    def porcentaje_aumento(self) -> float:
        return 0.01
    
    def puede_solicitar_promocion(self):
        return self.experiencia >= 5
    
    def to_dict(self):
        return {
            "tipo_empleado": type(self).__nombre__,
            "nombre": self.nombre,
            "dni": self.conseguir_dni(),
            "posicion": self.conseguir_posicion(),
            "salary": self.conseguir_salario(),
            "experiencia": self.experiencia,
            "esta_bloqueado": self.esta_bloqueado,
            "intentos_fallidos": self.intentos_fallidos,
            "puede_cambiar_rol": self.puede_cambiar_rol,
            "bloqueado_hasta": self.bloqueado_hasta.isoformat() if self.bloqueado_hasta else None
        }