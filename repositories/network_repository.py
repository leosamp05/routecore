import json
import os
from pathlib import Path

from models.location import Location
from models.road import Road

class NetworkRepository:
    def __init__(self, file_path: str) -> None:
        self.file_path = Path(file_path)
        self._ensure_file_exists()
        
        
    def _ensure_file_exists(self) -> None:
        self.file_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )
        
        if not self.file_path.exists():
            initial_data = {
                "locations": [],
                "roads": []
            }

            with self.file_path.open(
                "w",
                encoding="utf-8"
            ) as file:
                json.dump(
                    initial_data,
                    file,
                    indent=4,
                    ensure_ascii=False
                )
            
        
    def load_network(self) -> tuple[list[Location], list[Road]]:
        with self.file_path.open("r", encoding="utf-8") as file:
            data = json.load(file)
        
        locations = [
            Location(location['code'], location['name'])
            for location in data['locations']
        ]
        
        roads = [
            Road(
                road['origin'],
                road['destination'], 
                road['distance'], 
                road['status']
            )
            for road in data['roads']
        ]
            
        return locations, roads
    
    def save_network(self, locations: list[Location], roads: list[Road]) -> None:
        data = {
            "locations": [
                {
                    "name": location.name, 
                    "code": location.code
                }
                for location in locations
            ],
            "roads": [
                {
                    "origin": road.origin,
                    "destination": road.destination,
                    "distance": road.distance,
                    "status": road.status
                }
                for road in roads
            ]
        }
        
        temp_path = self.file_path.with_name(
            self.file_path.name + ".tmp"
        )
        
        try:
            with temp_path.open("w", encoding="utf-8") as file:
                json.dump(data, file, indent=4, ensure_ascii=False)
                
            os.replace(temp_path, self.file_path)
        except Exception:
            if temp_path.exists():
                temp_path.unlink()
            raise