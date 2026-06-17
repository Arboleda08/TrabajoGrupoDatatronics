from Modelos.AutenticableHelper.AutenticableHelper import AutenticableHelper
class SocioComercial:
    def __init__(self) -> None:
        self._helper = AutenticableHelper()
        self.clave: str | None = None

    def autenticar_usuario(self, clave: str) -> bool:
        return self._helper.comparar_claves(self.clave, clave)
    
    def to_dict(self):
        return {
            "clave": self.clave
        }