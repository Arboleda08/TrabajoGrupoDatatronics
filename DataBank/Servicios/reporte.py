from Servicios.Banco import Banco

class ObjetosDeInforme:
    def __init__(self, banco: "Banco"):
        self.banco = banco

    def generar_informe_de_empleado(self):
        reporte = []
        for empleado in self.banco.empleado:
          reporte.append({
              "Nombre": empleado.nombre,
              "Dni": empleado.obtener_dni(),
              "Rol": empleado.obtener_posicion(),
              "Salario": empleado.obtener_salario(),
              "Experiencia": empleado.experiencia,
              "Está bloqueado": empleado.esta_bloqueado
          })
        return reporte
  
    def generar_reporte_de_seguridad(self):
        print("Generando reporte de seguridad...")
        print("\n===== REPORTE DE SEGURIDAD =====\n")
        
        registros_fallidos = 0
        for registro in self.banco.registros:
            if registro.accion == "registro" and not registro.estatus:
                registros_fallidos += 1

        print (f"Total de logs: {len(self.banco.registros)}")
        print(f"Intentos de inicio de sesión fallidos: {registros_fallidos}")
        print(f"Saldo total del banco: {self.banco.obtener_dinero_total_banco()}")

        if registros_fallidos > 100:
            print("Alerta crítica: Se recomienda bloquear cuentas afectadas y auditar el sistema.")
        elif registros_fallidos > 50:
            print("Alerta alta: Se recomienda bloquear de forma temporal las cuentas afectadas.")
        elif registros_fallidos > 20:
            print("Alerta: Número alarmante de intentos fallidos. Tomar medidas inmediatas.")
        elif registros_fallidos > 10:
            print("Alerta: Demasiados intentos fallidos. Revisar la seguridad de las cuentas.")
        elif registros_fallidos > 3:
            print("Alerta: Múltiples intentos de inicio de sesión fallidos detectados.")
        else:
            print("Sin alertas de seguridad.")

        print("\nReporte de seguridad generado exitosamente.")

        return {
            "total_registros": len(self.banco.registros),
            "registros_fallidos": registros_fallidos
        }
      
    def generar_reporte_de_credito(self):
          print("Generando reporte de créditos...")
          print("\n===== REPORTE DE CRÉDITOS =====\n")
          reporte = []
          for cliente in self.banco.clientes:
            for credito in cliente.creditos:
                reporte.append({
                    "Cliente": cliente.nombre,
                    "Monto": credito.monto,
                    "Estado": credito.estatus,
                    "Tasa de interés": credito.tasa_de_interes,
                    "Meses": credito.moeses
                })
    
          print("Reporte de créditos generado exitosamente.")
          return reporte

    def generar_clientes_reporte(self):
        reporte = []

        for cliente in self.banco.clientes:
            reporte.append(str(cliente))

        return reporte


    def generar_reporte_de_cuentas(self):
        reporte = []

        for cuenta in self.banco.cuentas:
            reporte.append(str(cuenta))

        return reporte

    def generar_reporte_de_transaccion(self):
        reporte = []

        for transaccion in self.banco.global_transacciones:
            reporte.append(str(transaccion))

        return reporte

    def generar_reporte_financiero(self):
        total_balance = 0

        for cuenta in self.banco.cuentas:
            total_balance += cuenta.obtener_balance()

        return {
            "total_cuentas": len(self.banco.cuentas),
            "total_clientes": len(self.banco.clientes),
            "total_dinero": total_balance
        }
    
