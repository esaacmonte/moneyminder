class operation_does_not_exist(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message

    def __str__(self):
        return f"Erro: {self.message}"

    