class AutenticableHelper:
    def comparate_passwords(self, saved_password: str | None, written_password: str) -> bool:
        return saved_password == written_password