class Road:
    ALLOWED_STATUSES = {"OPEN", "CLOSED"}

    def __init__(
        self,
        origin: str,
        destination: str,
        distance: int | float,
        status: str,
    ) -> None:
        self._validate(origin, destination, distance, status)

        self.origin = origin.strip().upper()
        self.destination = destination.strip().upper()
        self.distance = distance
        self.status = status.strip().upper()

    @staticmethod
    def _validate(
        origin: str,
        destination: str,
        distance: int | float,
        status: str,
    ) -> None:
        if not isinstance(origin, str):
            raise TypeError("Origin must be a string.")

        if not origin.strip():
            raise ValueError("Origin cannot be empty.")

        if not isinstance(destination, str):
            raise TypeError("Destination must be a string.")

        if not destination.strip():
            raise ValueError("Destination cannot be empty.")

        if origin.strip().upper() == destination.strip().upper():
            raise ValueError("Origin and destination must be different.")

        if isinstance(distance, bool) or not isinstance(distance, (int, float)):
            raise TypeError("Distance must be a number.")

        if distance <= 0:
            raise ValueError("Distance must be positive.")

        if not isinstance(status, str):
            raise TypeError("Status must be a string.")

        normalized_status = status.strip().upper()

        if not normalized_status:
            raise ValueError("Status cannot be empty.")

        if normalized_status not in Road.ALLOWED_STATUSES:
            raise ValueError("Status must be 'OPEN' or 'CLOSED'.")
        
        
    def open(self) -> None:
        if self.status == "OPEN":
            raise ValueError("The road is already open.")
        self.status = "OPEN"
        
        
    def close(self) -> None:
        if self.status == "CLOSED":
            raise ValueError("The road is already closed.")
        self.status = "CLOSED"