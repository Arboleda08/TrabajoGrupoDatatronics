from Servicios.Banco import Banco
from Modelos.Cuentas.Credito import Credito
from Modelos.Cuentas.Cliente import Cliente
from Modelos.Roles.Empleado import Empleado
from Modelos.Excepciones.OperacionImposibleException import OperacionImposibleException

class AdministrarCreditos:
    def __init__(self, banco: "Banco"):
        self.banco = banco

    def solicitar_credito(self, cliente: Cliente, monto: float, meses: int):
        credito = Credito(monto, self.banco.tasa_interes, meses, cliente)
        return credito

    def aprobar_credito(self, empleado: "Empleado", cliente: Cliente, credito: Credito):
        if not empleado.puede_aprobar_credito(credito.monto):
            raise OperacionImposibleException("El empleado no tiene permisos para aprobar créditos.")
        
        if credito not in cliente.creditos:
            raise OperacionImposibleException("El crédito no pertenece a este cliente.")
            
        if credito.estatus != "Pendiente":
            raise OperacionImposibleException("Sólo se pueden aprobar créditos pendientes.")
            
        credito.aprobado = True
        credito.estatus = "Aprobado"

        return True
    
    def rechazar_credito(self, empleado: "Empleado", cliente: Cliente, credito: Credito):
        if credito not in cliente.creditos:
            raise ValueError("El crédito no pertenece a este cliente")
        
        if credito.estatus != "Pendiente":
            raise OperacionImposibleException("Sólo se pueden rechazar créditos pendientes")
        
        if cliente.edad > 65:
            credito.aprobado = False
            credito.estatus = "Rechazado"
            return "El cliente supera la edad máxima, el crédito ha sido rechazado."
        
        activo = []
        for cred in cliente.creditos:
            if cred.estatus == "Aprobado":
                activo.append(cred)
                
        if activo:
            credito.aprobado = False
            credito.estatus = "Rechazado"
            return "El cliente ya tiene un crédito aprobado, no puede solicitar otro."
        
        pendiente = []
        for cred in cliente.creditos:
            if cred == credito:
                continue

            if cred.remaining_balance > 0 and cred.status != "Rechazado":
                pendiente.append(cred)

        if pendiente:
            credito.aprobado = False
            credito.estatus = "Rechazado"
            return "El cliente tiene cuotas pendientes. Solicitud de crédito rechazada."
        
        cuentas_clientes = []
        for acc in self.banco.cuentas:
            if acc.cliente == cliente:
                cuentas_clientes.append(acc)

        encuentro = False
        for acc in cuentas_clientes:
            if acc.conseguir_balance() < 0:
                encuentro = True
                break
        if encuentro:
            credito.aprobado = False
            credito.estatus = "Rechazado"
            return "El cliente tiene saldo negativo en alguna cuenta. Crédito denegado."
        
        raise OperacionImposibleException ("No hay motivo para rechazar el crédito")

 
    def calcular_intereses_credito(self, credito: "Credito"):
        return credito.monto * credito.tasa_interes * (credito.meses / 12)

    def pagar_cuota_credito(self, cliente: "Cliente", credito: "Credito", monto: float):
        if credito not in cliente.creditos:
            raise ValueError("El crédito no pertenece a este cliente.")
   
        if credito.estatus != "Aprobado":
            raise OperacionImposibleException("El crédito no está activo.")
   
        if monto <= 0:
            raise ValueError("El monto de la cuota debe ser mayor a 0.")
   
        if monto > credito.restante_balance:
            monto = credito.restante_balance
   
        credito.restante_balance -= monto
   
        if credito.restante_balance <= 0:
            credito.restante_balance = 0
            credito.estatus = "Pagado"
   
        return credito.restante_balance
      