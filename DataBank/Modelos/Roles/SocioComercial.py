from Modelos.AyudanteAuténtico.AyudanteAuténtico import AyudanteAuténtico
class SocioComercial:
    def __init__(self) -> None:
        self._ayudante = AyudanteAuténtico()
        self.clave: str | None = None

    def autenticar_usuario(self, clave: str) -> bool:
        return self._helper.comparar_contraseñas(self.clave, clave)
    
    def to_dict(self):
        return {
            "clave": self.clave
        }
