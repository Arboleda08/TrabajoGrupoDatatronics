class AyudadorAutenticable:
    def comparar_contraseñas(self, contraseña_guardada: str | None, contraseña_escrita: str) -> bool:
        return contraseña_guardada == contraseña_escrita