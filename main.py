from cli.main_menu import main_menu
from repositories.network_repository import NetworkRepository
from services.network_service import NetworkService
from services.route_service import RouteService


repository = NetworkRepository("./data/network.json")
network_service = NetworkService(repository)
route_service = RouteService(network_service)


main_menu(route_service, network_service)