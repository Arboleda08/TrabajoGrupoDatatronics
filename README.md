# DataBank
Este proyecto consiste en un banco virtual, donde, a través de clases para las cuentas bancarias y roles de una empresa, se manejan inversiones, flujos de dinero, créditos e incluso, ascensos. Buscamos crear un programa integral donde, mediante funcionalidades básicas de un banco y gestión de personal en una empresa, sea sencillo administrar clientes, cuentas, transacciones y empleados desde un mismo sistema.
Este proyecto se está desarrollando bajo el paradigma de POO (Programación Orientada a Objetos), implementando conceptos como herencia, encapsulamiento, polimorfismo, encapsulamiento y composición. Además, se hace uso de manejo de excepciones, autenticaci+on de usuarios, control de permisos según roles, entre otros.

Por el momento, DataBank permite:
- Crear y administrar distintos tipos de cuentas bancarias.
- Gestionar clientes y empleados.
- Realizar depósitos, retiros y transferencias.
- Llevar historiales de transacciones y actividad del cliente.
- Controlar autenticación según el rol dentro de la empresa.
- Gestionar ascensos y salarios de empleados.
  
## Paquete Modelos
Este paquete contiene la mayor parte de módulos de nuestro banco. Tiene cuatro subpaquetes, a saber: Autenticable Helper, Cuentas, Excepciones, Log y Roles. 
A continuación, breves detalles sobre cada uno de ellos:

### Autenticable Helper
Este subpaquete contiene un módulo que ayuda en el manejo de contraseñas, puesto que verifica si la contraseña almacenada en el sistema coincide con la que se ingresa. Es por ello que la denominamos "helper", ya que más que un objeto extra, nos facilita los procesos de autenticación de personal y cuentas.

```python
class AutenticableHelper:
    def comparate_passwords(self, saved_password: str | None, written_password: str) -> bool:
        return saved_password == written_password
```

### Cuentas
Este subpaquete contiene todos los tipos de cuentas bancarias que ofrece nuestro banco. Como base, tomamos la clase CuentaBancaria, que contiene los datos básicos de una cuenta en la vida real, como número de banco, cliente y número de cuenta. En suma, contiene todas las transacciones posibles dentro del banco, junto con un límite de transacciones por minuto y un espacio de registro de las transacciones.

```python
from .Cliente import Cliente
from Modelos.Cuentas.Transaccion import Transaction
from Modelos.Excepciones.SaldoInsuficienteException import SaldoInsuficienteException
from Modelos.Excepciones.OperacionImposibleException import OperacionImposibleException
import uuid
from datetime import datetime
from datetime import timedelta

class CuentaBancaria:
    account_count: int = 0

    def __init__(self, bank_number: int, client: Cliente, account_number: int | None = None):
        if bank_number is None or bank_number <= 0:
            raise ValueError("Es obligatorio un número de agencia válido")
        if account_number is not None and account_number <= 0:
            raise ValueError("Es obligatorio ingresar el número de cuenta")

        self.bank_number = bank_number
        self.account_number = (
            account_number if account_number is not None
            else str(uuid.uuid4())[:8]
        )
        self.client = client
        self._balance: float = 0.0
        self.interest_rate: float = 0.0
        self.overdraft_limit: float = 0.0
        self.account_active: bool = False
        self.commission_value: float = 0.0
        self.__withdrawals_without_balance: int = 0
        self.__transfers_without_balance: int = 0
        self.transactions: list["Transaction"] = []
        self.max_transactions_per_minute = 1
        self.creation_date = datetime.now()

        CuentaBancaria.account_count += 1

    def get_balance(self) -> float:
        return self._balance

    def get_withdrawals_without_balance(self) -> int:
        return self.__withdrawals_without_balance

    def get_transfers_without_balance(self) -> int:
        return self.__transfers_without_balance
    
    def get_min_balance(self)-> float:
        return 0

    def get_max_transactions_per_minute(self):
        return self.max_transactions_per_minute
    
    def can_withdraw(self, amount: float)-> bool:
        if self._balance - amount < self.get_min_balance():
            return False
        return True
    
    def daily_withdraws(self):
        today = datetime.now().date()
        return [
        t for t in self.transactions
        if t.type == "Retiro" and t.date.date() == today
        ]
    
    def check_transaction_limit(self):
        now = datetime.now()
        one_minute_ago = now - timedelta(minutes=1)

        recent = [
            t for t in self.transactions
            if t.date >= one_minute_ago
        ]

        if len(recent) >= self.get_max_transactions_per_minute():
            raise OperacionImposibleException("Límite excedido")

    def withdraw(self, amount: float) -> bool:
        self.check_transaction_limit()
        
        if amount <= 0:
            raise ValueError("Monto inválido")

        if not self.can_withdraw(amount):
            self.__withdrawals_without_balance += 1
            raise SaldoInsuficienteException("No puede superar el límite de la cuenta")

        self._balance -= amount
        withdraw = Transaction(type="Retiro", amount= amount, origin_acc=self, destination_acc= None, description=f"Retiro de: ${amount}")
        self.transactions.append(withdraw)
        return True

    def deposit(self, amount: float) -> None:
        self.check_transaction_limit()
        if amount < 0:
            raise ValueError("Es imposible depositar un valor negativo.")
        
        self._balance += amount
        deposit = Transaction(type="Depósito", amount= amount, origin_acc=self, destination_acc= None, description=f"Depósito de: ${amount}")
        self.transactions.append(deposit)

    def transfer(self, amount: float, target_account: "CuentaBancaria") -> float:
        try:
            self.withdraw(amount)
        except SaldoInsuficienteException as ex:
            self.__transfers_without_balance += 1
            print("Transferencia inválida", ex)
        target_account.deposit(amount)

        transfer = Transaction(type="Transferencia", amount=amount, origin_acc= self, destination_acc= target_account, description=f"Transferencia de ${amount} a la cuenta: {target_account}")
        self.transactions.append(transfer)
        return self._balance

    def show_history(self):
        for x in self.transactions:
            print(x)

    def __str__(self) -> str:
        return (f"Número de cuenta: {self.account_number}\n"
                f"Número de banco: {self.bank_number}\n"
                f"DNI: {self.client.dni}\n"
                f"Nombre del cliente: {self.client.name}\n"
                f"Saldo: {self._balance}")
```

### Cuenta Ahorros
A diferencia de la CuentaBancaria, CuentaAhorros tiene una tasa de interés distinta, al igual que número de retiros disponibles por día.

```python
from Modelos.Cuentas.CuentaBancaria import CuentaBancaria
from Modelos.Excepciones.OperacionImposibleException import OperacionImposibleException
from Modelos.Cuentas.Cliente import Cliente

class CuentaAhorros(CuentaBancaria):
    def __init__(self, bank_number: int, client: Cliente, account_number: int | None = None):
        super().__init__(bank_number, client, account_number)
        self.interest_rate = 0.5
        self.daily_withdrawal_limit = 6
        
    def apply_interest_rate(self):
        self._balance += self._balance * self.interest_rate

    def withdraw(self, amount: float) -> bool:
        if amount <=0:
            raise OperacionImposibleException("Monto Inválido")
        
        if amount > self.get_balance():
            raise OperacionImposibleException("La cuenta de ahorros no permite saldo negativo")
        
        return super().withdraw(amount)
    
    def get_max_transactions_per_minute(self):
        return 2
    
    def can_withdraw(self, amount):
        return (
            len(self.daily_withdraws()) < self.daily_withdrawal_limit
            and self._balance - amount >= 0
        )    
```

### Cuenta Corriente
Presenta una sutil diferencia entre CuentaAhorros, puesto que aquí la diferencia es que el cliente puede tener un saldo negativo, hasta cierto tope estipulado por el banco.

```python
from Modelos.Cuentas.CuentaBancaria import CuentaBancaria
from Modelos.Excepciones.OperacionImposibleException import OperacionImposibleException
from Modelos.Cuentas.Cliente import Cliente

class CuentaCorriente(CuentaBancaria):
    def __init__(self, bank_number: int, client: Cliente, account_number: int | None = None):
        super().__init__(bank_number, client, account_number)
        self.overdraft_limit = -500
    
    def get_min_balance(self):
        return self.overdraft_limit
    
    def withdraw(self, amount: float) -> bool:
        if amount <=0:
            raise OperacionImposibleException("Monto Inválido")
        
        if self.get_balance() - amount < self.overdraft_limit:
            raise OperacionImposibleException("Límite de sobregiro excedido")
        
        return super().withdraw(amount)
    
    def get_max_transactions_per_minute(self):
        return 2
    
    def can_withdraw(self, amount):
        return self._balance - amount >= self.get_min_balance()
```

### Cuenta Empresarial
Este tipo de cuenta sólo puede ser creada por usuarios autorizados, tiene un nit, límite de retiro mayor al de cuqlueir otra cuenta, y un límite aún mayor de deuda.

```python
from Modelos.Cuentas.CuentaBancaria import CuentaBancaria
from Modelos.Cuentas.Cliente import Cliente

class CuentaEmpresarial(CuentaBancaria):
    def __init__(self, bank_number: int, client: Cliente, nit: int, authorized_users: list["Cliente"], account_number: int | None = None):
        super().__init__(bank_number, client, account_number)
        self.nit = nit
        self.authorized_users = authorized_users
        self.overdraft_limit = -10000
        self.daily_withdrawal_limit = 100
    
    def add_authorized_user(self, new_user: "Cliente"):
        self.authorized_users.append(new_user)
    
    def get_max_transactions_per_minute(self):
        return 10
    
    def can_withdraw(self, amount):
        return (
            len(self.daily_withdraws()) < self.daily_withdrawal_limit
            and self._balance - amount >= 0
        )    
```

### Cuenta Juvenil
Tiene un límite específico de edad para ser creada, junto al monto de dinero que puede ser almacenado y el número de operaciones que pueden realizarse por día.

``` python
from Modelos.Cuentas.CuentaBancaria import CuentaBancaria
from Modelos.Cuentas.Cliente import Cliente
from Modelos.Excepciones.OperacionImposibleException import OperacionImposibleException

class CuentaJuvenil(CuentaBancaria):
    def __init__(self, bank_number: int, client: Cliente, account_number: int | None = None):
        if not (13<= client.age <=20):
            raise OperacionImposibleException("Sólo clientes entre 13 y 20 años pueden tener una cuenta juvenil.")
        
        super().__init__(bank_number, client, account_number)
        self.daily_withdrawal_limit = 5
    
    def can_withdraw(self, amount):
        return (
            len(self.daily_withdraws()) < self.daily_withdrawal_limit
            and self._balance - amount >= 0
        )    
```

### Cliente
Es la clase base de una persona dentro del banco. Contiene datos personales como nombre, dni, edad, profesion e historial crediticio.

```python
class Cliente:
    def __init__(self, name: str, dni: int, age: int, profession: str):
        self.name = name
        self.dni = dni
        self.age = age
        self.profession = profession
        self.credits = []

    def add_credit(self, credit):
        self.credits.append(credit)

    def __str__(self) -> str:
        return f"Cliente: {self.name}, Dni: {self.age}"
```

### Credito
Modela un crédito bancario con monto, tasa de interés, cliente, estado de aprobación, entre otros.

```python
from Modelos.Cuentas.Cliente import Cliente

class Credito:
    def __init__(self, amount: float, interest_rate: float, months: int, client: Cliente):
        self.amount = amount
        self.interest_rate = interest_rate
        self.months = months
        self.client = client
        self.approved = False
        self.remaining_balance = amount
        self.status = "Pendiente de aprobación."
        client.add_credit(self)

    def __str__(self) -> str:
        return (f"Credito de {self.amount} para {self.client.name}")
```

### Transacción
Crea un código único para cada transacción, de modo que puede ser detallada su información relativa a monto, cuentas de destino y origen, fecha. Contiene una función __str__ que permite visualizar el contenido de una operación.

```python
from Modelos.Cuentas.CuentaBancaria import CuentaBancaria
import uuid
from datetime import datetime
class Transaction:
    def __init__(self, type: str, amount: float, origin_acc: "CuentaBancaria", destination_acc, description: str):
        self.id = uuid.uuid4().hex[:8]
        self.date = datetime.now()
        self.type = type
        self.amount = amount
        self.origin_account = origin_acc
        self.destination_account = destination_acc
        self.description = description

    def __str__(self) -> str:
        return (
            f"Id transacción: {self.id}\n"
            f"Fecha de la transacción: {self.date}\n"
            f"Tipo de la transacción: {self.type}\n"
            f"Monto de dinero: {self.amount}\n"
            f"Cuenta de destino: {self.destination_account}\n"
            f"Detalles y descripción: {self.description}\n"
            )
```

## Excepciones
Creamos dos excepciones personalizadas, pues son explícitas y facilitan la lectura de código. Estas son:

- CuentaNoEncontradaException
  
```python
class CuentaNoEncontradaException(Exception):
    pass
```

-OperacionImposibleException

```python
class OperacionImposibleException(Exception):
    def __init__(self, message: str = "Error en operación financiera", codigo: int | None = None):
        super().__init__(message)
        self.codigo = codigo

    def __str__(self):
        if self.codigo:
            return f"[Error {self.codigo}] {super().__str__()}"
        return super().__str__()
```

-SaldoInsuficienteException

```python
class SaldoInsuficienteException(Exception):
    pass
```
