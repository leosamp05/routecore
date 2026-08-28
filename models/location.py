class Location:
    def __init__(self, code: str, name: str) -> None:
        self._validate(code, name)

        self.code = code.strip().upper()
        self.name = name.strip()

    @staticmethod
    def _validate(code: str, name: str) -> None:
        if not isinstance(code, str):
            raise TypeError("Code must be a string.")

        if not code.strip():
            raise ValueError("Code cannot be empty.")

        if not isinstance(name, str):
            raise TypeError("Name must be a string.")

        if not name.strip():
            raise ValueError("Name cannot be empty.")