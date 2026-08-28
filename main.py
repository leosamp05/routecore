from repositories.network_repository import NetworkRepository
from services.network_service import NetworkService


repository = NetworkRepository("./data/network.json")
network_service = NetworkService(repository)