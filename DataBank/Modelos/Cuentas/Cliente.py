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

