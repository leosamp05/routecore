from algorithms.dijkstra import dijkstra
from services.network_service import NetworkService

class RouteService:
    def __init__(self, network_service: NetworkService) -> None:       
        self.network_service = network_service
   
    def calculate(self, origin: str, destination: str) -> tuple[list[str], int | float] | None:
        origin_location = self.network_service.get_location(origin)
        destination_location = self.network_service.get_location(destination)
        
        graph = self.network_service.build_graph()
        
        result = dijkstra(graph, origin_location.code, destination_location.code)
        
        return result