from Servicios.Banco import Banco
from Modelos.Roles.Empleado import Empleado

class SearchObjects:
    def __init__(self, bank: "Banco"):
        self.bank = bank

    def search_client_by_dni(self, dni: int):
        for client in self.bank.clients:
            if client.dni == dni:
                return client

        return (f"No se encontró un cliente con el dni {dni}.")
    
    def search_client_by_name(self, name: str):
        for client in self.bank.clients:
            if client.name == name:
                return client

        return (f"No se encontró un cliente con el nombre {name}.")

    def search_account_by_number(self, number: int):
        for account in self.bank.accounts:
            if account.account_number == number:
                return account

        return(f"No se encontró una cuenta con el número {number}.")

    def search_employee_by_dni(self, dni: int):
        for employee in self.bank.employees:
            if employee.get_dni() == dni:
                return employee

        return (f"No se encontró un empleado con el dni {dni}.")
    
    def search_employee_by_name(self, name: str):
        for employee in self.bank.employees:
            if employee.name == name:
                return employee

        return (f"No se encontró un empleado con el nombre {name}.")

    def search_account_by_bank(self, bank: int):
        accounts = []

        for account in self.bank.accounts:
            if account.bank_number == bank:
                accounts.append(account)

        return accounts    
    
    def promotion_history(self, employee: "Empleado"):
        result = []
        for log in self.bank.logs:
            if log.employee == employee and log.action == "Promoción":
                result.append(log)
        return result
    
    def employee_activity_history(self, employee: "Empleado"):
        history = []
        for log in self.bank.logs:
            if log.employee == employee:
                history.append(log)
        
        return history
    
    def employee_login_history(self, employee: "Empleado"):
        history = []
        for log in self.bank.logs:
              if log.employee == employee and log.action == "login":
                  history.append(log)

        return history
    
    def filter_transactions_by_type(self, transaction_type: str):
        valid_types = ["Retiro", "Depósito", "Transferencia"]
        if transaction_type not in valid_types:
            raise ValueError(f"Tipo inválido. Los tipos válidos son: {valid_types}")
        
        found = []
        for t in self.bank.global_transactions:
            if t.type == transaction_type:
                found.append(t)

        return found
      
    def filter_transactions_by_amount(self, min_amount: float, max_amount: float):
        if min_amount < 0 or max_amount < 0:
            raise ValueError("Los montos no pueden ser negativos.")
        if min_amount > max_amount:
            raise ValueError("El monto mínimo no puede ser mayor al máximo.")
        
        found = []
        for t in self.bank.global_transactions:
            if min_amount <= t.amount <= max_amount:
                found.append(t)
        return found
    
        
