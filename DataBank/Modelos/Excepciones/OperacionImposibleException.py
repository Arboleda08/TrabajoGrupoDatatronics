class OperacionImposibleException(Exception):
    def __init__(self, message: str = "Error en operación financiera", codigo: int | None = None):
        super().__init__(message)
        self.codigo = codigo

    def __str__(self):
        if self.codigo:
            return f"[Error {self.codigo}] {super().__str__()}"
        return super().__str__()