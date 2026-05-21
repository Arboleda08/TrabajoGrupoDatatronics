from Modelos.AutenticableHelper.AutenticableHelper import AutenticableHelper
class SocioComercial:
    def __init__(self) -> None:
        self._helper = AutenticableHelper()
        self.clave: str | None = None

    def autenticar_usuario(self, clave: str) -> bool:
        return self._helper.comparate_passwords(self.clave, clave)