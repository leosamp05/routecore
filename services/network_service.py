from models.location import Location
from models.road import Road
from repositories.network_repository import NetworkRepository

class NetworkService:
    def __init__(self, repository: NetworkRepository) -> None:
        self.repository = repository
        self.locations, self.roads = self.repository.load_network()
        
        
    @staticmethod
    def _normalize_code(value: str, field_name: str) -> str:
        if not isinstance(value, str):
            raise TypeError(f"{field_name} must be a string.")
        if not value.strip():
            raise ValueError(f"{field_name} cannot be empty.")

        return value.strip().upper()
    
    def _location_exists(self, code: str) -> bool:
        return any(location.code == code for location in self.locations)
    
    def _road_exists(self, origin: str, destination: str) -> bool:
        return any(
            (road.origin == origin and road.destination == destination) 
            or 
            (road.origin == destination and road.destination == origin)
            for road in self.roads
        )
        
    def _save_network(self) -> None:
        self.repository.save_network(
            self.locations,
            self.roads
        )
    
    
    def get_location(self, code: str) -> Location:
        code = self._normalize_code(code, 'Code')
        
        for location in self.locations:
            if location.code == code:
                return location
            
        raise ValueError("No Location with this code.")
        
    def get_road(self, origin: str, destination: str) -> Road:
        origin = self._normalize_code(origin, 'Origin')
        destination = self._normalize_code(destination, 'Destination')
        
        for road in self.roads:
            if (
                road.origin == origin and road.destination == destination 
                or 
                road.origin == destination and road.destination == origin
            ):
                return road
        
        raise ValueError(f"No Road with Origin: {origin} and Destination: {destination}.")
    
    
    def add_location(self, code: str, name: str) -> Location:
        new_location = Location(code, name)
        
        if self._location_exists(new_location.code):
            raise ValueError("Location already exists.")
        
        self.locations.append(new_location)
        try:
            self._save_network()
        except Exception:
            self.locations.pop()
            raise
        
        return new_location
    
    def add_road(self, origin: str, destination: str, distance: int | float, status: str) -> Road:
        new_road = Road(origin, destination, distance, status)
        
        if not self._location_exists(new_road.origin):
            raise ValueError("Origin does not exist.")
        if not self._location_exists(new_road.destination):
            raise ValueError("Destination does not exist.")
        
        if self._road_exists(new_road.origin, new_road.destination):
            raise ValueError("Road already exists.")

        self.roads.append(new_road)
        try:
            self._save_network()
        except Exception:
            self.roads.pop()
            raise
        
        return new_road
    
    
    def open_road(self, origin: str, destination: str) -> None:
        road = self.get_road(origin, destination)
        road.open()
        try:
            self._save_network()
        except Exception:
            road.close()
            raise
        
    def close_road(self, origin: str, destination: str) -> None:
        road = self.get_road(origin, destination)
        road.close()
        try:
            self._save_network()
        except Exception:
            road.open()
            raise
    
    
    def build_graph(self) -> dict[str, dict[str, int | float]]:
        graph = {}
        
        for location in self.locations:
            graph[location.code] = {}
            
        for road in self.roads:
            if road.status == "OPEN":
                graph[road.origin][road.destination] = road.distance
                graph[road.destination][road.origin] = road.distance
            
        return graph