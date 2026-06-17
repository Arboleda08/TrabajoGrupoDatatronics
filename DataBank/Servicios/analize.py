from Servicios.Banco import Banco
from Modelos.Cuentas.Cliente import Cliente
from Modelos.Cuentas.CuentaBancaria import CuentaBancaria
from Modelos.Cuentas.CuentaAhorros import CuentaAhorros
from Modelos.Cuentas.CuentaCorriente import CuentaCorriente
from Modelos.Cuentas.CuentaEmpresarial import CuentaEmpresarial
from Modelos.Cuentas.CuentaJuvenil import CuentaJuvenil
from Modelos.Cuentas.Transaction import Transaccion
from Modelos.Excepciones.OperacionImposibleException import OperacionImposibleException
from Modelos.Roles.Empleado import Empleado

class Analizar:
    def __init__(self, banco: "Banco"):
        self.banco = banco

    def conseguir_dinero_total_del_banco(self):
          total_dinero = 0
          for cuenta in self.banco.cuentas:
              total_dinero += cuenta.conseguir_balance()
          return total_dinero
    
    def conseguir_total_transacciones(self):
          return len(self.banco.global_transacciones)

    def detectar_operaciones_sospechosas(self):
        cuenta_sospechosa = []

        for cuenta in self.banco.cuentas:
            if (cuenta.obtener_retiros_sin_saldo() >= 3):
                cuenta_sospechosa.append(cuenta)

        return cuenta_sospechosa
    
    def conseguir_tipo_cuenta_mas_utilizado(self):
        if not self.banco.cuentas:
            return None
        
        ahorros = 0
        corriente = 0
        empresarial = 0
        juvenil = 0

        for cuenta in self.banco.cuentas:
            if isinstance(cuenta, CuentaAhorros):
                ahorros += 1
            elif isinstance(cuenta, CuentaCorriente):
                corriente += 1
            elif isinstance(cuenta, CuentaEmpresarial):
                empresarial += 1
            elif isinstance(cuenta, CuentaJuvenil):
                juvenil += 1

        if ahorros >= corriente and ahorros >= empresarial and ahorros >= juvenil:
            return "CuentaAhorros"
        elif corriente >= empresarial and corriente >= juvenil:
            return "CuentaCorriente"
        elif empresarial >= juvenil:
            return "CuentaEmpresarial"
        else:
            return "CuentaJuvenil"
    
    def conseguir_top_clientes(self, n: int):
        if n <= 0:
            raise ValueError("n debe ser mayor a 0.")
        cliente_balances = []
        for cliente in self.banco.clientes:
            total = sum(
                cuenta.get_balance()
                for cuenta in self.banco.cuentas
                if cuenta.cliente == cliente
            )
            cliente_balances.append((cliente, total))
        cliente_balances.sort(key=lambda x: x[1], reverse=True)
        return [cliente for cliente, _ in cliente_balances[:n]]
    
    def clasificar_cliente(self, cliente: "Cliente"):
        total_balance = sum(
            cuenta.conseguir_balance()
            for cuenta in self.banco.cuentas
            if cuenta.cliente == cliente
        )
        if total_balance >= 100000:
            return "VIP"
        elif total_balance >= 10000:
            return "Preferencial"
        else:
            return "Básico"
          
    def calcular_cliente_puntaje(self, client: "Cliente"):
        puntaje = 0.0
        total_balance = 0.0
            
        for cuenta in self.banco.cuentas:
              if cuenta.cliente == client:
                  total_balance += cuenta.conseguir_balance()

        if total_balance/1000 < 300:
          puntaje += total_balance/1000
        else:
          puntaje +=300

        creditos_pagados = [c for c in Cliente.creditos if c.estatus == "Pagado"]
        puntaje += len(creditos_pagados) * 50

        creditos_rechazados = [c for c in Cliente.creditos if c.estatus == "Rechazado"]
        puntaje -= len(creditos_rechazados) * 30

        if puntaje < 0:
            return 0

        return round(puntaje)
  
    def conversión_moneda(self, monto: float, de_moneda: str, a_moneda: str, tarifas: dict):
          # Convierte un monto entre monedas usando un diccionario de tasas respecto al USD.
          if de_moneda not in tarifas or a_moneda not in tarifas:
              raise ValueError(f"Moneda no soportada. Disponibles: {list(tarifas.keys())}")
          if monto <= 0:
              raise ValueError("El monto debe ser mayor a 0.")
          amount_in_base = monto / tarifas[de_moneda]
          converted = amount_in_base * tarifas[a_moneda]
          return round(converted, 2)
    
    def detectar_transacciones_grandes(self, limite: float):
        transacciones_grandes = []

        for transaccion in self.banco.global_transacciones:
            if transaccion.monto > limite:
                transacciones_grandes.append(transaccion)

        return transacciones_grandes
    
    def detectar_logins_sospechosos(self, empleado: "Empleado"):
        return empleado.intentos_fallidos >= 3
    
