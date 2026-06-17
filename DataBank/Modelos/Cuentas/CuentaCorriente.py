from Modelos.Cuentas.CuentaBancaria import CuentaBancaria
from Modelos.Excepciones.OperacionImposibleException import OperacionImposibleException
from Modelos.Cuentas.Cliente import Cliente

class CuentaCorriente(CuentaBancaria):
    def __init__(self, numero_bancario: int, client: Cliente, numero_de_cuenta: int | None = None):
        super().__init__(numero_bancario, client, numero_de_cuenta)
        self.limite_de_sobregiro = -500
    
    def conseguir_minimo_balance(self):
        return self.limite_de_sobregiro
    
    def retirar(self, monto: float) -> bool:
        if monto <=0:
            raise OperacionImposibleException("Monto Inválido")
        
        if self.obtener_balance() - monto < self.conseguir_minimo_balance():
            raise OperacionImposibleException("Límite de sobregiro excedido")
        
        return super().retirar(monto)
    
    def obtener_maximo_transacciones_por_minuto(self):
        return 2
    
    def puede_retirar(self, monto: float):
        return self._balance - monto >= self.conseguir_minimo_balance()