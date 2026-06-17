from Servicios.Banco import Banco
from Modelos.Roles.Empleado import Empleado

class BuscarObjetos:
    def __init__(self, banco: "Banco"):
        self.banco = banco

    def buscar_cliente_por_dni(self, dni: int):
        for cliente in self.banco.clientes:
            if cliente.dni == dni:
                return cliente

        return (f"No se encontró un cliente con el dni {dni}.")
    
    def buscar_cliente_por_nombre(self, nombre: str):
        for cliente in self.banco.clientes:
            if cliente.nombre == nombre:
                return cliente

        return (f"No se encontró un cliente con el nombre {nombre}.")

    def buscar_cuenta_por_numero(self, numero: int):
        for cuenta in self.banco.cuentas:
            if cuenta.numero_de_cuenta == numero:
                return cuenta

        return(f"No se encontró una cuenta con el número {numero}.")

    def buscar_empleado_por_dni(self, dni: int):
        for empleado in self.banco.empleados:
            if empleado.obtener_dni() == dni:
                return empleado

        return (f"No se encontró un empleado con el dni {dni}.")
    
    def buscar_empleado_por_nombre(self, nombre: str):
        for empleado in self.banco.empleados:
            if empleado.nombre == nombre:
                return empleado

        return (f"No se encontró un empleado con el nombre {nombre.")

    def buscar_cuenta_por_banco(self, banco: int):
        cuentas = []

        for cuenta in self.banco.cuentas:
            if cuenta.numero_bancario == banco:
                cuentas.append(cuenta)

        return cuentas    
    
    def historial_promoción(self, empleado: "Empleado"):
        resultado = []
        for registro in self.banco.registros:
            if registro.empleado == empleado and registro.accion == "Promoción":
                resultado.append(registro)
        return resultado
    
    def empleado_historial_de_actividad(self, empleado: "Empleado"):
        historial = []
        for registro in self.banco.registros:
            if registro.empleado == empleado:
                historial.append(registro)
        
        return historial
    
    def empleado_historial_de_registro(self, empleado: "Empleado"):
        historial = []
        for registro in self.banco.registros:
              if registro.empleado == empleado and registro.accion == "registro":
                  historial.append(registro)

        return historial
    
    def filtrar_transacciones_por_tipo(self, tipo_de_transaccion: str):
        tipos_validados = ["Retiro", "Depósito", "Transferencia"]
        if tipo_de_transaccion not tipos_validados:
            raise ValueError(f"Tipo inválido. Los tipos válidos son: {tipos_validados}")
        
        encontro = []
        for t in self.banco.global_transacciones:
            if t.type == tipo_de_transaccion:
                encontro.append(t)

        return encontro
      
    def filtrar_transacciones_por_monto(self, monto_minimo: float, monto_maximo: float):
        if monto_minimo < 0 or monto_maximo < 0:
            raise ValueError("Los montos no pueden ser negativos.")
        if monto_minimo > monto_maximo:
            raise ValueError("El monto mínimo no puede ser mayor al máximo.")
        
        encontro = []
        for t in self.banco.global_transacciones:
            if monto_minimo <= t.monto <= monto_maximo:
                encontro.append(t)
        return encontro
    
        
