class Cliente:
    def __init__(self, nombre: str, dni: int, edad: int, profesion: str):
        self.nombre = nombre
        self.dni = dni
        self.edad = edad
        self.profesion = profesion
        self.creditos = []
        self.esta_lista_negra = False
        self.razon_lista_negra = ""

    def añadir_credito(self, credito):
        self.creditos.append(credito)

    def __str__(self) -> str:
        return f"Cliente: {self.nombre}, Dni: {self.edad}"

    def to_dict(self):
        return {
            "nombre": self.nombre,
            "dni": self.dni,
            "edad": self.edad,
            "profesion": self.profesion,
            "esta_lista_negra": self.esta_lista_negra,
            "razon_lista_negra": self.razon_lista_negra,
            "creditos": [credito.to_dict() for credito in self.creditos]
        }