from Modelos.Cuentas.Cliente import Cliente
from Modelos.Roles.Empleado import Empleado
from Servicios.Banco import Banco

class ListaObjetos:
    def __init__(self, banco: "Banco"):
        self.banco = banco

    def list_client(self, empleado: "Empleado"):
        self.banco.validate_permission(empleado, "Ver_informacion")

        return self.banco.clientes
    
    def list_accounts(self, empleado: "Empleado"):
        self.banco.validate_permission(empleado, "Ver_informacion")

        return self.banco.cuentas

    def listar_cuentas_por_cliente(self, cliente: "Cliente"):
        cuentas = []

        for cuenta in self.banco.cuentas:
            if cuenta.cliente == cliente:
                cuentas.append(cuenta)

        return cuentas

    def listar_cuentas_por_banco(self, nuevo_número_banco: int):
        cuentas = []

        for cuenta in self.banco.cuentas:
            if cuenta.número_bancario == nuevo_número_banco:
                cuentas.append(cuenta)

        return cuentas

    def listar_empleados(self, empleado: "Empleado"):
        self.banco.validar_permiso(empleado, "Ver_informacion")

        return self.banco.empleados

    def listar_creditos_activos(self):
          creditos_activos = []
          for client in self.banco.clientes:
              for credit in client.creditos:
                  if credit.estado == "Aprobado":
                      creditos_activos.append(credit)
          return creditos_activos
    
    def listar_tarjetas(self):
        tarjetas = []
        for cuenta in self.banco.cuentas:
            for tarjeta in cuenta.tarjetas:
                tarjetas.append(tarjeta)
        return tarjetas
    
    def listar_tarjetas_por_cliente(self, cliente: "Cliente"):
        tarjetas = []
        for cuenta in self.banco.cuentas:
            if cuenta.cliente == cliente:
                for tarjeta in cuenta.tarjetas:
                    tarjetas.append(tarjeta)
        return tarjetas
        
    
    
