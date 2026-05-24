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
En caso de que se intente acceder a una cuenta que no existe o se tenga por detino una cuenta que no se encuentra en la memoria.
  
```python
class CuentaNoEncontradaException(Exception):
    pass
```

- OperacionImposibleException
En caso de que se intente tener un saldo negativo, hacer alguna operación que no le corresponde según su tipo de empleado, realizar más de cierta cantidad de retiros diaria, etc.

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

- SaldoInsuficienteException
Cuando el usuario intente transferir o retirar un monto con el que no cuenta, sale esta excepción.

```python
class SaldoInsuficienteException(Exception):
    pass
```

## Log
<p>Este paquete contiene a la clase Log, la cual simplifica el registro de veces accedidas por el usuario al sistema.</p>

```python
import uuid
from Modelos.Roles.Empleado import Empleado
from datetime import datetime

class Log:
    def __init__(self, empleado: Empleado, accion: str, estado: str, detalle: str = ""):
        self.id = uuid.uuid4().hex[:8]
        self.fecha = datetime.now()

        self.empleado = empleado
        self.accion = accion
        self.estado = estado   
        self.detalle = detalle
```

## Roles
<p>Este paquete es vital dentro de nuestro proyecto, puesto que contiene los 7 tipos de clientes que se tendrán en la empresa. Por obvias razones, están sujetos a cambios y creación de otros nuevos. </p>

### Empleado

<p>Éste es la clase base que contiene atributos propios de una persona contratada por una entidad, al igual que funcionalidades como solicitar aumento de salario, bonus, despedir o contratar empleados, etc. Algunos de los métodos son sobreescritos en clases posteriores, ya que según el rango al que se pertenezca, se limitan las capacidades.</p>

```python
class Empleado:
    total_employees: int = 0
    
    def __init__(self, name: str, dni: int, position: str, salary: float, experience: int) -> None:
        Empleado.total_employees +=1
        self.name = name
        self.__position = position
        self.__dni = dni
        self.__salary = salary
        self.experience = experience
        self.is_blocked = False
        self.failed_attempts = 0

    def get_position(self):
        return (self.__position)
    
    def set_position(self, new_position):
        self.__position = new_position

    def get_dni(self):
        return (self.__dni)
    
    def get_salary(self):
        return (self.__salary)
    
    def set_salary(self, new_salary):
        self.__salary = new_salary
    
    def obtain_bonus(self) -> float:
        raise NotImplementedError("El método debe ser implementado en la sublclase.")

    def raise_salary(self):
        self.set_salary(
            self.get_salary() * (1 + self.percentage_increase())
        )
    
    def can_approve_credit(self, amount: float)-> bool:
        return False
    
    def can_modify_salary(self, employee: "Empleado", amount: float)-> bool:
        return False
    
    def can_see_reports(self) ->bool:
        return False
    
    def can_see_information(self) -> bool:
        return False
    
    def can_approve_transfer(self, amount: float) -> bool:
        return False
    
    def can_create_user(self) -> bool:
        return False
    
    def can_delete_user(self) ->bool:
        return False
    
    def can_raise_salary(self, employee: "Empleado") -> bool:
        return False
    
    def percentage_increase(self) -> float:
        return 0.01
    
    def can_request_promotion(self):
        return self.experience >= 5
```

### Empleado Autenticable
<p> Hereda de empleado. Su diferencia radica en que EmpleadoAutenticable cuenta con contraseña y sistema de verificación de la misma.</p>

```python
from Modelos.Roles.Empleado import Empleado
from Modelos.AutenticableHelper.AutenticableHelper import AutenticableHelper

class EmpleadoAutenticable(Empleado):
    def __init__(self, name: str, dni: int, position: str, salary: float, experience: int, password: str):
        super().__init__(name, dni, position, salary, experience)
        self._helper = AutenticableHelper()
        self.password = password

    def authenticate_user(self, new_password: str):
        return self._helper.comparate_passwords(self.password, new_password)

    def obtain_bonus(self) -> float:
        return 0
```

### Administrativo
<p>Cualquier empleado que sea ejecutivo o jefe gozará de estas funcionalidades. Puede ver reportes, ver información, crear y eliminar usuarios. Como novedad, tiene un aumento de salario distinto al de un empleado base.</p>

```python
from Modelos.Roles.EmpleadoAutenticable import EmpleadoAutenticable
class Administrativo(EmpleadoAutenticable):
    def __init__(self, name: str, dni: int, experience: int, password: str):
        super().__init__(name, dni, "Administrativo", 20000, experience, password)

    def obtain_bonus(self):
        return self.get_salary() * 0.15
    
    def can_see_reports(self) ->bool:
        return True
    
    def can_see_information(self) -> bool:
        return True
    
    def can_create_user(self) -> bool:
        return True
    
    def can_delete_user(self) ->bool:
        return True
    
    def percentage_increase(self) -> float:
        return 0.08
```

### Analista
<p>Ve reportes y tiene un bono diferente al resto de empleados. </p>

```python
from Modelos.Roles.EmpleadoAutenticable import EmpleadoAutenticable
class Analista(EmpleadoAutenticable):
    def __init__(self, name: str, dni: int, experience: int, password: str):
        super().__init__(name, dni, "Analista", 30000, experience, password)
    
    def obtain_bonus(self):
        return self.get_salary() * 0.2
    
    def can_see_reports(self) -> bool:
        return True
    
    def percentage_increase(self) -> float:
        return 0.08
```

### Director
<p> Similar a Administrativo. No obstante, puede aprobar transferencias y créditos, subir y modificar salarios de otros empleados y obtener bonos más altos que otros empleados.</p>

```python
from Modelos.Roles.EmpleadoAutenticable import EmpleadoAutenticable
from Modelos.Roles.Empleado import Empleado
class Director(EmpleadoAutenticable):
    def __init__(self, name: str, dni: int, department: str, experience: int, password: str):
        super().__init__(name, dni, "Director", 50000, experience, password)
        self.department = department

    def obtain_bonus(self):
        return self.get_salary() * 0.5

    def can_approve_credit(self, amount: float)-> bool:
        return amount <= 100000
    
    def can_modify_salary(self, employee: "Empleado", amount: float)-> bool:
        return amount <= 0.2 * employee.get_salary()
    
    def can_see_reports(self) ->bool:
        return True
    
    def can_see_information(self) -> bool:
        return True
    
    def can_approve_transfer(self, amount: float) -> bool:
        return amount <= 50000
    
    def can_create_user(self) -> bool:
        return True
    
    def can_delete_user(self) ->bool:
        return True
    
    def can_raise_salary(self, employee: "Empleado") -> bool:
        return True
    
    def percentage_increase(self) -> float:
        return 0.06
```

### Logistica
<p>Sólo difiere su porcentaje de incremento de salario y bonus.</p>

```python
from Modelos.Roles.EmpleadoAutenticable import EmpleadoAutenticable
class Logistica(EmpleadoAutenticable):
    def __init__(self, name: str, dni: int, experience: int, password: str):
        super().__init__(name, dni, "Logística", 15000, experience, password)

    def obtain_bonus(self):
        return self.get_salary()* 0.3
    
    def percentage_increase(self) -> float:
        return 0.02
```

### Socio Comercial
<p>Usuario con contraseña. Tendrá privilegios en transferencias, créditos e inversiones. </p>

```python
from Modelos.AutenticableHelper.AutenticableHelper import AutenticableHelper
class SocioComercial:
    def __init__(self) -> None:
        self._helper = AutenticableHelper()
        self.clave: str | None = None

    def autenticar_usuario(self, clave: str) -> bool:
        return self._helper.comparate_passwords(self.clave, clave)
```

## Servicios
<p>Este paquete contiene lo que hasta ahora ha sido la parte principal de nuestro proyecto. Aquí se han establecido relaciones de jerarquía entre empleados, al igual que operaciones permitidas entre cuentas. </p>

### Bonus Admin
<p>Módulo dedicado al bonus del salario del empleado</p>

```python
from Modelos.Roles.Empleado import Empleado
class BonusAdmin:
    def __init__(self) -> None:
        self.__total_bonus: float = 0.0

    def register(self, employee: Empleado):
        self.__total_bonus += employee.obtain_bonus()

    def get_total_bonus(self):
        return self.__total_bonus
```

### Banco
<p>Es la entidad central del sistema (por no decir que constituye casi la totalidad del sistema). Autentica usuarios, los bloquea, valida permisos para crear y eliminar usuarios, ver reportes e información. De igual forma, almecena los registros de los clientes, las transacciones, cuentas bancarias, entre otras.
Cuenta con acciones básicas como búsqueda de clientes por dni y número de banco.</p>
<p>Para gestionar los empleados, se pueden despedir (dependiendo si el cargo lo permite), cambiar su rol (lo que simula un ascenso), se aprueban incrementos de salario, se modifica experiencia y se detectan operaciones sospechosas.</p>
<p>Como extra, se utilizó una función especial con la librería json para exportar las cuentas en este formato.</p>
<p>Próximamente, se actualizarán funcionalidades relativas a créditos e inversiones, más será necesario realizar otras clases para que Banco no se convierta en una superclase.</p>

```python
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
```
