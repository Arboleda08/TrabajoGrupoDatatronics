from Servicios.Banco import Banco

class ReportObjects:
    def __init__(self, bank: "Banco"):
        self.bank = bank

    def generate_employee_report(self):
        report = []
        for employee in self.bank.employees:
          report.append({
              "Nombre": employee.name,
              "Dni": employee.get_dni(),
              "Rol": employee.get_position(),
              "Salario": employee.get_salary(),
              "Experiencia": employee.experience,
              "Está bloqueado": employee.is_blocked
          })
        return report
  
    def generate_security_report(self):
        print("Generando reporte de seguridad...")
        print("\n===== REPORTE DE SEGURIDAD =====\n")
        
        failed_logins = 0
        for log in self.bank.logs:
            if log.action == "login" and not log.status:
                failed_logins += 1

        print (f"Total de logs: {len(self.bank.logs)}")
        print(f"Intentos de inicio de sesión fallidos: {failed_logins}")
        print(f"Saldo total del banco: {self.bank.get_total_bank_money()}")

        if failed_logins > 100:
            print("Alerta crítica: Se recomienda bloquear cuentas afectadas y auditar el sistema.")
        elif failed_logins > 50:
            print("Alerta alta: Se recomienda bloquear de forma temporal las cuentas afectadas.")
        elif failed_logins > 20:
            print("Alerta: Número alarmante de intentos fallidos. Tomar medidas inmediatas.")
        elif failed_logins > 10:
            print("Alerta: Demasiados intentos fallidos. Revisar la seguridad de las cuentas.")
        elif failed_logins > 3:
            print("Alerta: Múltiples intentos de inicio de sesión fallidos detectados.")
        else:
            print("Sin alertas de seguridad.")

        print("\nReporte de seguridad generado exitosamente.")

        return {
            "total_logs": len(self.bank.logs),
            "failed_logins": failed_logins
        }
      
    def generate_credit_report(self):
          print("Generando reporte de créditos...")
          print("\n===== REPORTE DE CRÉDITOS =====\n")
          report = []
          for client in self.bank.clients:
            for credit in client.credits:
                report.append({
                    "Cliente": client.name,
                    "Monto": credit.amount,
                    "Estado": credit.status,
                    "Tasa de interés": credit.interest_rate,
                    "Meses": credit.months
                })
    
          print("Reporte de créditos generado exitosamente.")
          return report

    def generate_clients_report(self):
        report = []

        for client in self.bank.clients:
            report.append(str(client))

        return report


    def generate_accounts_report(self):
        report = []

        for account in self.bank.accounts:
            report.append(str(account))

        return report

    def generate_transactions_report(self):
        report = []

        for transaction in self.bank.global_transactions:
            report.append(str(transaction))

        return report

    def generate_financial_report(self):
        total_balance = 0

        for account in self.bank.accounts:
            total_balance += account.get_balance()

        return {
            "total_accounts": len(self.bank.accounts),
            "total_clients": len(self.bank.clients),
            "total_money": total_balance
        }
    
