import json
from Modelos.Cuentas.Cliente import Cliente
from Modelos.Cuentas.Credito import Credito
from Modelos.Cuentas.CuentaBancaria import CuentaBancaria
from Modelos.Cuentas.CuentaAhorros import CuentaAhorros
from Modelos.Cuentas.CuentaCorriente import CuentaCorriente
from Modelos.Cuentas.CuentaEmpresarial import CuentaEmpresarial
from Modelos.Cuentas.CuentaJuvenil import CuentaJuvenil
from Modelos.Cuentas.Cliente import Cliente
from Modelos.Cuentas.Transaccion import Transaction
from Modelos.Roles.Empleado import Empleado
from Modelos.Roles.EmpleadoAutenticable import EmpleadoAutenticable
from Modelos.Roles.Director import Director
from Modelos.Roles.Administrativo import Administrativo
from Modelos.Roles.Analista import Analista
from Modelos.Roles.Logistica import Logistica
from Modelos.Excepciones.SaldoInsuficienteException import SaldoInsuficienteException
from Modelos.Excepciones.OperacionImposibleException import OperacionImposibleException
from Modelos.Log.Log import Log
from Servicios.BonusAdmin import BonusAdmin
from datetime import datetime, timedelta

class Banco:
    def __init__(self, name: str, clients: list[Cliente], employees: list[Empleado], global_transactions: list[Transaction], logs: list[Log], bonus_admin: BonusAdmin):
        self.name = name
        self.clients = clients
        self.employees = employees
        self.accounts: list[CuentaBancaria] = []
        self.global_transactions = global_transactions
        self.logs = logs
        self.bonus_admin = bonus_admin
        self.interest_rate = 0.6

    def autenticate_user(self, employee: "EmpleadoAutenticable", password: str):
        if employee.authenticate_user(password):
            return True

        self.verify_failed_attempt(employee)
        return False

    def block_employee(self, employee: "Empleado"):
        employee.is_blocked= True


    def unblock_employee(self, employee: "Empleado"):
        employee.is_blocked = False
        employee.failed_attempts = 0

    def validate_permission(self, employee: "Empleado", action: str, obj: object):
        permissions = {
            "create_client": employee.can_create_user(),
            "delete_account": employee.can_delete_user(),
            "see_information": employee.can_see_information(),
            "see_reports": employee.can_see_reports(),
        }

        if action not in permissions:
            raise OperacionImposibleException("Operación inválida")
        
        if not permissions[action]:
            raise PermissionError(
                f"{employee.name} no tiene permiso para {action}"
            )
        
        return True

    def verify_failed_attempt(self, employee: "Empleado"):
        employee.failed_attempts +=1

        if employee.failed_attempts >= 3:
            self.block_employee(employee)

    def create_client(self, employee: "Empleado", client_data):
        self.validate_permission(employee, "create_client", None)

        client = Cliente (
            client_data["name"],
            client_data["dni"],
            client_data["age"],
            client_data["profession"]
        )

        self.clients.append(client)
        return client

    def upgrade_client(self, employee: "Empleado", client: "Cliente", account_type: str):
        self.validate_permission(employee, "create_client", client)

        account = self.create_account(
            employee,
            client,
            account_type
        )

        return account

    def search_client_by_dni(self, dni: int):
        for client in self.clients:
            if client.dni == dni:
                return client

        return None

    def list_client(self, employee: "Empleado"):
        self.validate_permission(employee, "see_information", None)

        return self.clients

    def create_account(self, employee: "Empleado", client: "Cliente", account_type: str):
        self.validate_permission(employee, "create_client", client)

        account_types = {
            "savings": CuentaAhorros,
            "current": CuentaCorriente,
            "business": CuentaEmpresarial,
            "student": CuentaJuvenil
        }

        if account_type not in account_types:
            raise ValueError("Invalid account type")

        account_class = account_types[account_type]

        account = account_class(
            agency_number="0001"
        )

        account.client = client

        self.accounts.append(account)

        return account

    def delete_account(self, employee: "Empleado", account: CuentaBancaria):
        self.validate_permission(employee, "delete_account", account)

        if account in self.accounts:
            self.accounts.remove(account)
            return True

        return False

    def search_account_by_number(self, number: int):
        for account in self.accounts:
            if account.account_number == number:
                return account

        return None

    def list_accounts(self, employee: "Empleado"):
        self.validate_permission(employee, "see_information", None)

        return self.accounts

    def list_accounts_by_client(self, client: "Cliente"):
        accounts = []

        for account in self.accounts:
            if account.client == client:
                accounts.append(account)

        return accounts

    def list_accounts_by_bank(self, new_bank_number: int):
        accounts = []

        for account in self.accounts:
            if account.bank_number == new_bank_number:
                accounts.append(account)

        return accounts

    def change_account_status(self, employee: "Empleado", account: CuentaBancaria):
        self.validate_permission(employee, "delete_account", account)

        account.account_active = not account.account_active

        return account.account_active

    def register_transaction(self, transaction: "Transaction"):
        self.global_transactions.append(transaction)

    def get_account_history(self, account: CuentaBancaria):
        return account.transactions

    def get_client_history(self, client: "Cliente"):
        transactions = []

        for account in self.accounts:
            if account.client == client:
                for transaction in account.transactions:
                    transactions.append(transaction)

        return transactions

    def get_global_transactions(self, employee: "Empleado"):
        return self.global_transactions

    def create_employee(self, employee: "Empleado", data, role: str):
        self.validate_permission(employee, "create_user", None)

        roles = {
            "administrative": Administrativo,
            "analyst": Analista,
            "director": Director,
            "logistic": Logistica
        }

        if role not in roles:
            raise ValueError("Invalid role")

        role_class = roles[role]

        new_employee = role_class(
            data["name"],
            data["dni"],
            data["experience"],
            data["password"]
        )

        self.employees.append(new_employee)

        return new_employee

    def delete_employee(self, employee: "Empleado", target):
        self.validate_permission(employee, "delete_user", target)
        if target in self.employees:
            self.employees.remove(target)
            return True

        return False


    def change_role(self, employee: "Empleado", target, new_role: str):
        self.validate_permission(employee, "create_user", target)
        target.set_position(new_role)

        return target.get_position()

    def list_employees(self, employee: "Empleado"):
        self.validate_permission(employee, "see_information", None)

        return self.employees

    def search_employee(self, dni: int):
        for employee in self.employees:
            if employee.get_dni() == dni:
                return employee

        return None

    def approve_salary_increase(self, employee: "Empleado", target, amount: float):
        if not employee.can_modify_salary(target, amount):
            raise PermissionError("No es posible modificar el salario.")

        target.set_salary(target.get_salary() + amount)

        return target.get_salary()


    def apply_salary_increase(self, employee: "Empleado", target: "Empleado"):
        if not employee.can_raise_salary(target):
            raise PermissionError("No es posible aumentar el salario.")
        
        target.raise_salary()

        return target.get_salary()

    def register_global_bonus(self):
        for employee in self.employees:
            self.bonus_admin.register(employee)

    def get_total_bonus(self):
        return self.bonus_admin.get_total_bonus()

    def request_promotion(self, employee: "Empleado"):
        return employee.can_request_promotion()

    def approve_promotion(self, director: "Director", employee: "Empleado"):
        if not director.can_create_user():
            raise OperacionImposibleException("Permiso denegado.")

        employee.experience += 1

        return True

    def update_experience(self, employee: "Empleado", points: int):
        employee.experience += points

        return employee.experience

    def generate_clients_report(self):
        report = []

        for client in self.clients:
            report.append(str(client))

        return report


    def generate_accounts_report(self):
        report = []

        for account in self.accounts:
            report.append(str(account))

        return report

    def generate_transactions_report(self):
        report = []

        for transaction in self.global_transactions:
            report.append(str(transaction))

        return report

    def generate_financial_report(self):
        total_balance = 0

        for account in self.accounts:
            total_balance += account.get_balance()

        return {
            "total_accounts": len(self.accounts),
            "total_clients": len(self.clients),
            "total_money": total_balance
        }

    def sort_accounts_by_number(self):
        self.accounts.sort(key=lambda account: account.account_number)

        return self.accounts

    def sort_accounts_by_balance(self):
        self.accounts.sort(key=lambda account: account.get_balance())

        return self.accounts
    
    def search_by_dni(self, new_dni: int):
        for client in self.clients:
            if client.dni == new_dni:
                return client

        return (f"No se encontró un cliente con el dni {new_dni}.")

    def search_by_account_number(self, new_number: int):
        for account in self.accounts:
            if account.account_number == new_number:
                return account
        
        return(f"No se encontró una cuenta con el número {new_number}.")

    def search_by_bank(self, bank: int):
        accounts = []

        for account in self.accounts:
            if account.bank_number == bank:
                accounts.append(account)

        return accounts

    def register_log(self, action, employee: "Empleado", result):
        log = Log(employee, action, result)
        self.logs.append(log)
        
        return log

    def get_logs(self):
        return self.logs

    def detect_suspicious_operations(self):
        suspicious_accounts = []

        for account in self.accounts:
            if (account.get_withdrawals_without_balance() >= 3):
                suspicious_accounts.append(account)

        return suspicious_accounts

    def export_accounts_json(self):
        data = []

        for account in self.accounts:
            data.append({
                "account number": account.account_number,
                "bank number": account.bank_number,
                "client": account.client.name,
                "balance": account.get_balance()
            })
        with open("accounts.json", "w") as file:
            json.dump(
                data,
                file,
                indent=4
            )

    def request_credit(self, client: Cliente, amount: float, months: int):
        credit = Credito(amount, self.interest_rate, months, client)
        return credit

    def approve_credit(self, client: Cliente, credit: Credito):
        credit.approved = True
        credit.status = "Aprobado"
        client.credits.append(credit)

    def reject_credit(self):
        #Rechaza una solicitud de crédito y registra el motivo.
        if Credito in Cliente.credits:
            Credito.approved = False
            Credito.status = "Rechazado"
            Credito.rejection_reason = "Motivo de rechazo"
        elif Credito not in Cliente.credits:
             raise ValueError("El cliente no tiene una solicitud de crédito.")
        elif self.interest_rate > 0.5:
            Credito.approved = False
            Credito.status = "Rechazado"
            Credito.rejection_reason = "Tasa de interés excesiva"
        elif self.amount < self.interest_rate * 1000:
            Credito.approved = False
            Credito.status = "Rechazado"
            Credito.rejection_reason = "Monto solicitado demasiado alto"
        elif credits in self.clients.credits and credits.status == "Aprobado":
            Credito.approved = False
            Credito.status = "Rechazado"
            Credito.rejection_reason = "El cliente ya tiene un crédito aprobado"
        elif Cliente.age < 18:
            Credito.approved = False
            Credito.status = "Rechazado"
            Credito.rejection_reason = "El cliente no cumple con la edad mínima"
        elif Cliente.age > 65:
            Credito.approved = False
            Credito.status = "Rechazado"
            Credito.rejection_reason = "El cliente supera la edad máxima"
        elif Cliente.profession in ["Desempleado", "Informal"]:
            Credito.approved = False
            Credito.status = "Rechazado"
            Credito.rejection_reason = "La profesión del cliente no es elegible"
        elif Cliente.get_score() < 600:
            Credito.approved = False
            Credito.status = "Rechazado"
            Credito.rejection_reason = "El cliente tiene un puntaje crediticio insuficiente"
        elif self.dni in self.clients or self.name in self.clients or self.client in self.clients or self.age in self.clients or self.profession in self.clients:
            if self.dni != self.dni:
                Credito.approved = False
                Credito.status = "Rechazado"
                Credito.rejection_reason = "Los Datos no coinciden con los registrados"
            elif self.name != self.name:
                Credito.approved = False
                Credito.status = "Rechazado"
                Credito.rejection_reason = "Los Datos no coinciden con los registrados"
            elif self.client != self.client:
                Credito.approved = False
                Credito.status = "Rechazado"
                Credito.rejection_reason = "Los Datos no coinciden con los registrados"
            elif self.age != self.age:
                Credito.approved = False
                Credito.status = "Rechazado"
                Credito.rejection_reason = "Los Datos no coinciden con los registrados"
            elif self.profession != self.profession:
                Credito.approved = False
                Credito.status = "Rechazado"
                Credito.rejection_reason = "Los Datos no coinciden con los registrados"

        else:
            raise OperacionImposibleException("No se puede rechazar el crédito.")
    
    def calculate_credit_interest(self):
        #Calcula los intereses totales de un crédito.
        credit_interest = Credito.amount * Credito.interest_rate * (Credito.months / 12)
        return credit_interest
        

    def pay_credit_installment(self, client: "Cliente", credit: "Credito", amount: float):
        # Permite pagar una cuota de un crédito activo.
        if credit not in client.credits:
            raise ValueError("El crédito no pertenece a este cliente.")
 
        if credit.status != "Aprobado":
            raise OperacionImposibleException("El crédito no está activo.")
 
        if amount <= 0:
            raise ValueError("El monto de la cuota debe ser mayor a 0.")
 
        if amount > credit.remaining_balance:
            amount = credit.remaining_balance
 
        credit.remaining_balance -= amount
 
        if credit.remaining_balance <= 0:
            credit.remaining_balance = 0
            credit.status = "Pagado"
 
        return credit.remaining_balance.
        
    def list_active_credits(self):
        # Retorna todos los créditos actualmente activos (aprobados y no pagados).
        active_credits = []
        for client in self.clients:
            for credit in client.credits:
                if credit.status == "Aprobado":
                    active_credits.append(credit)
        return active_credits

    def create_card(self, client: Cliente, account: CuentaBancaria):
        #Genera una tarjeta asociada a una cuenta bancaria.
        Tarjeta = self.create_card(client, account)
        account.cards.append(Tarjeta)
        return Tarjeta

    def block_card(self, card):
        #Bloquea una tarjeta para impedir su uso.
        card.blocked = True

    def unblock_card(self, card):
        #Reactiva una tarjeta previamente bloqueada.
        card.blocked = False

    def change_card_pin(self, card, new_pin: str):
        #Cambia el PIN de seguridad de una tarjeta.
        card.pin = new_pin

    def list_cards(self):
        #Muestra todas las tarjetas asociadas a un cliente o cuenta.
        pass

    def validate_card(self):
        if self.block_card:
            return False
        elif self.card_expired():
            return False
        else: 
            return True
        #Verifica si una tarjeta es válida y está activa.

    def create_investment(self):
        #Permite crear una inversión asociada a un cliente.
        pass

    def calculate_investment_profit(self):
        #Calcula las ganancias generadas por una inversión.
        pass

    def withdraw_investment(self):
        #Retira parcial o totalmente una inversión.
        pass

    def list_investments(self):
        #Lista las inversiones registradas.
        pass

    def send_notification(self, notification_type: str, message: str):
        #Envía una notificación al cliente o empleado.
        notification_types = ["client", "employee"]
        message = f"Notificación: {message}"
        if notification_type not in notification_types:
            raise ValueError("Invalid notification type")
        elif notification_type == "client":
            print(f"Notificación enviada al cliente: {message}")
        elif notification_type == "employee":
            print(f"Notificación enviada al empleado: {message}")
        pass #crear

    def notify_large_transfer(self):
        if Transaction > self.validate_transfer_limit():
            self.message = "Se ha detectado una transferencia grande."
            self.send_notification("client", "Se ha detectado una transferencia grande.")

    def notify_login(self):
        if self.suspicious_login_detection():
            self.message = "Se ha detectado un inicio de sesión sospechoso."
            self.send_notification("client", "Se ha detectado un inicio de sesión sospechoso.")

    def notify_account_blocked(self):
        if self.block_card:
            self.message = "Su tarjeta ha sido bloqueada."
            self.send_notification("client", "Su tarjeta ha sido bloqueada.")
    
    def detect_multiple_logins(self):
        if self.client_login_history() > 3:
            self.message = "Se han detectado múltiples inicios de sesión."
            self.send_notification("client", "Se han detectado múltiples inicios de sesión.")

    def detect_large_transactions(self):
        if self.global_transactions > self.validate_transfer_limit():
            self.message = "Se han detectado transacciones grandes."
            self.send_notification("client", "Se han detectado transacciones grandes.")

    def temporary_account_lock(self, employee: "Empleado", minutes: int):
        # Bloquea temporalmente a un empleado por una cantidad de minutos.
        if minutes <= 0:
            raise ValueError("Los minutos deben ser mayor a 0.")
        self.block_employee(employee)
        employee.locked_until = datetime.now() + timedelta(minutes=minutes)
        return employee.locked_until 

    def suspicious_login_detection(self):
        if self.employee_login_history() > 3:
            return True
        elif self.password_attempts() > 3:
            return True
        elif self.unusual_location_login():
            return True
        elif self.password_change_history() > 3:
            return True
        elif self.password != self.password:
            return True

    
    def validate_transfer_limit(self, amount: float, limit: float):
        # Verifica si el monto de transferencia supera el límite permitido.
        if amount <= 0:
            raise ValueError("El monto debe ser mayor a 0.")
        return amount <= limit
    
    def get_top_clients(self, n: int):
        # Retorna los n clientes con mayor saldo total entre todas sus cuentas.
        if n <= 0:
            raise ValueError("n debe ser mayor a 0.")
        client_balances = []
        for client in self.clients:
            total = sum(
                account.get_balance()
                for account in self.accounts
                if account.client == client
            )
            client_balances.append((client, total))
        client_balances.sort(key=lambda x: x[1], reverse=True)
        return [client for client, _ in client_balances[:n]]
        
    def get_total_bank_money(self):
        total_money = 0
        for account in self.accounts:
            total_money += account.get_balance()
        return total_money
        
    def get_total_transactions(self):
        return len(self.global_transactions)

    def get_most_used_account_type(self):
        # Retorna el tipo de cuenta más usado entre todas las cuentas registradas.
        if not self.accounts:
            return None
        type_count = {}
        for account in self.accounts:
            account_type = type(account).__name__
            type_count[account_type] = type_count.get(account_type, 0) + 1
        return max(type_count, key=type_count.get)

    def get_employee_performance(self, employee: "Empleado"):
        # Calcula el rendimiento de un empleado según sus acciones en logs.
        actions = [log for log in self.logs if log.employee == employee]
        successful = [log for log in actions if log.result == "success"]
        return {
            "employee": employee.name,
            "total_actions": len(actions),
            "successful_actions": len(successful),
            "performance_rate": round(len(successful) / len(actions), 2) if actions else 0.0
        }

    def close_account(self, employee: "Empleado", account: "CuentaBancaria"):
        # Cierra una cuenta bancaria si su saldo es cero.
        self.validate_permission(employee, "delete_account", account)
        if account.get_balance() != 0:
            raise OperacionImposibleException(
                "No se puede cerrar una cuenta con saldo pendiente."
            )
        account.account_active = False
        self.accounts.remove(account)
        self.register_log("close_account", employee, "success")
        return True

    def apply_monthly_fee(self, employee: "Empleado", account: "CuentaBancaria", fee: float):
        # Descuenta una comisión mensual al saldo de la cuenta.
        self.validate_permission(employee, "delete_account", account)
        if not account.account_active:
            raise OperacionImposibleException("La cuenta no está activa.")
        if fee <= 0:
            raise ValueError("La comisión debe ser mayor a 0.")
        account.withdraw(fee)
        self.register_log("apply_monthly_fee", employee, "success")
        return account.get_balance()

    def currency_conversion(self, amount: float, from_currency: str, to_currency: str, rates: dict):
        # Convierte un monto entre monedas usando un diccionario de tasas respecto al USD.
        if from_currency not in rates or to_currency not in rates:
            raise ValueError(f"Moneda no soportada. Disponibles: {list(rates.keys())}")
        if amount <= 0:
            raise ValueError("El monto debe ser mayor a 0.")
        amount_in_base = amount / rates[from_currency]
        converted = amount_in_base * rates[to_currency]
        return round(converted, 2)
    
    def promotion_history(self, employee: "Empleado"):
        # Retorna el historial de promociones de un empleado desde los logs.
        return [
            log for log in self.logs
            if log.employee == employee and log.action == "promotion"
        ]

    def reject_promotion(self):
        if self.approve_promotion == False:
            self.message = "Su solicitud de promoción ha sido rechazada."
            self.send_notification("employee", "Su solicitud de promoción ha sido rechazada.")
        else:
            raise OperacionImposibleException("No se puede rechazar la promoción.")
    
    def evaluate_promotion(self, director: "Director", employee: "Empleado"):
        # Evalúa si un empleado cumple los requisitos para ser promovido.
        if not director.can_create_user():
            raise OperacionImposibleException("Permiso denegado.")
        if not employee.can_request_promotion():
            return {
                "eligible": False,
                "reason": "El empleado no cumple los requisitos mínimos para solicitar promoción."
            }
        performance = self.get_employee_performance(employee)
        if performance["performance_rate"] < 0.7:
            return {
                "eligible": False,
                "reason": f"Rendimiento insuficiente: {performance['performance_rate']*100}%."
            }
        return {
            "eligible": True,
            "reason": "El empleado cumple todos los requisitos para ser promovido."
        }
    
    def generate_employee_report(self):
        # Genera un reporte con la información de todos los empleados.
        report = []
        for employee in self.employees:
            report.append({
                "name": employee.name,
                "dni": employee.get_dni(),
                "role": employee.get_position(),
                "salary": employee.get_salary(),
                "experience": employee.experience,
                "is_blocked": employee.is_blocked
            })
        return report

    def generate_security_report(self):
        print("Generando reporte de seguridad...")
        print("/n===== REPORTE DE SEGURIDAD =====/n")
        print(f"Intentos de inicio de sesión fallidos: {self.total_logs}")
        print(f"Saldo actual: {self.get_total_bank_money()}")
        print(f"Cuenta bloqueada: {self.block_card}")
        failed_logins = 0
        for log in self.logs:
            if log.action == "login" and log.result == "failed":
                failed_logins += 1
        return {
            "total_logs": len(self.logs),
            "failed_logins": failed_logins
        }
        if failed_logins > 3:
            print("Alerta: Se han detectado múltiples intentos de inicio de sesión fallidos.")
        elif failed_logins > 10:
            print("Alerta: Se han detectado demasiados intentos de inicio de sesión fallidos. Se recomienda revisar la seguridad de las cuentas.")
        elif failed_logins > 20:
            print("Alerta: Se han detectado un número alarmante de intentos de inicio de sesión fallidos. Se recomienda tomar medidas inmediatas para proteger las cuentas.")
        elif failed_logins > 50:
            print("Alerta: Se han detectado un número crítico de intentos de inicio de sesión fallidos. Se recomienda bloquear temporalmente las cuentas afectadas y revisar la seguridad del sistema.")
        elif failed_logins > 100:
            print("Alerta: Se han detectado un número extremadamente alto de intentos de inicio de sesión fallidos. Se recomienda bloquear permanentemente las cuentas afectadas y realizar una auditoría completa de seguridad.")
        else:
            print("No se han creado reportes de seguridad.")
        print("Reporte de seguridad generado exitosamente.")
        print
    def generate_suspicious_activity_report(self):
        print("Generando reporte de actividades sospechosas...")
        print("/n===== REPORTE DE ACTIVIDADES SOSPECHOSAS =====/n")
        print(f"Número de transacciones sospechosas: {len(self.detect_suspicious_operations())}")
        print(f"Transacciones sospechosas: {self.detect_suspicious_operations()}")
        #Genera un reporte detallado de actividades sospechosas detectadas tales como transacciones grandeso varias transacciones pequeñas.
        if self.transaction in self.global_transactions and self.transaction.amount > self.validate_transfer_limit():
            self.message = "Se ha detectado una transacción sospechosa."
            self.send_notification("client", "Se ha detectado una transacción sospechosa.")
        elif self.Detect_large_transactions():
            self.message = "Se han detectado transacciones sospechosas."
            self.send_notification("client", "Se han detectado transacciones sospechosas.")
        else:
            print("No se han detectado actividades sospechosas.")
        pass # transacciones sospechosas
        print("Reporte de actividades sospechosas generado exitosamente.")
    
    def generate_credit_report(self):
        print("Generando reporte de créditos...")
        print("/n===== REPORTE DE CRÉDITOS =====/n")
        for client in self.clients:
            print(f"Cliente: {client.name}")
            for credit in client.credits:
                print(f"  Monto: {credit.amount}, Estado: {credit.status}, Tasa de interés: {credit.interest_rate}, Meses: {credit.months}")
        print("Reporte de créditos generado exitosamente.")
        pass # historial de vida financiera del cliente, tarjetas, créditos, inversiones, deuda, etc.
    
    def filter_transactions_by_type(self, transaction_type: str):
        # Me filtra las transacciones globales por tipo ("Retiro", "Depósito", "Transferencia").
        valid_types = ["Retiro", "Depósito", "Transferencia"]
        if transaction_type not in valid_types:
            raise ValueError(f"Tipo inválido. Los tipos válidos son: {valid_types}")
        return [
            t for t in self.global_transactions
            if t.type == transaction_type
        ]
    
    def filter_transactions_by_amount(self, min_amount: float, max_amount: float):
        # Filtra las transacciones globales dentro de un rango de monto.
        if min_amount < 0 or max_amount < 0:
            raise ValueError("Los montos no pueden ser negativos.")
        if min_amount > max_amount:
            raise ValueError("El monto mínimo no puede ser mayor al máximo.")
        return [
            t for t in self.global_transactions
            if min_amount <= t.amount <= max_amount
        ]

    def classify_client(self, client: "Cliente"):
        # Clasifica al cliente según su saldo total: Básico, Preferencial o VIP.
        total_balance = sum(
            account.get_balance()
            for account in self.accounts
            if account.client == client
        )
        if total_balance >= 100000:
            return "VIP"
        elif total_balance >= 10000:
            return "Preferencial"
        else:
            return "Básico"
            
    def blacklist_client(self, employee: "Empleado", client: "Cliente", reason: str):
        # Agrega al cliente a una lista negra interna del banco y registra el motivo.
        self.validate_permission(employee, "delete_account", client)
        if not hasattr(client, "is_blacklisted"):
            client.is_blacklisted = False
        client.is_blacklisted = True
        client.blacklist_reason = reason
        self.register_log(
            "blacklist_client",
            employee,
            f"Cliente {client.name} (DNI: {client.dni}) bloqueado. Motivo: {reason}"
        )
        return True
    
    def calculate_client_score(self, client: "Cliente"):
        # Calcula un puntaje crediticio del cliente basado en saldo, créditos y edad.
        score = 0
        # Hasta 300 puntos por saldo total
        total_balance = sum(
            account.get_balance()
            for account in self.accounts
            if account.client == client
        )
        score += min(total_balance / 1000, 300)
        # 50 punto por cada crédito pagado
        paid_credits = [c for c in client.credits if c.status == "Pagado"]
        score += len(paid_credits) * 50
        # -30 puntos por cada crédito rechazado
        rejected_credits = [c for c in client.credits if c.status == "Rechazado"]
        score -= len(rejected_credits) * 30
        # +100 puntos si tiene 25 o más años
        if client.age >= 25:
            score += 100
        return max(0, round(score))
        
     def employee_activity_history(self, employee: "Empleado"):
        # Retorna todas las acciones registradas en logs para un empleado.
        return [log for log in self.logs if log.employee == employee]

     def employee_login_history(self, employee: "Empleado"):
        # Retorna el historial de inicios de sesión de un empleado desde los logs.
        return [
            log for log in self.logs
            if log.employee == employee and log.action == "login"
        ]

     def evaluate_employee(self, director: "Director", employee: "Empleado"):
        # Evalúa a un empleado con base en su rendimiento, experiencia y estado.
        if not director.can_see_reports():
            raise OperacionImposibleException("Permiso denegado.")
        performance = self.get_employee_performance(employee)
        login_history = self.employee_login_history(employee)
        return {
            "name": employee.name,
            "experience": employee.experience,
            "is_blocked": employee.is_blocked,
            "total_logins": len(login_history),
            "total_actions": performance["total_actions"],
            "successful_actions": performance["successful_actions"],
            "performance_rate": performance["performance_rate"]
        }
