from services.network_service import NetworkService
from services.route_service import RouteService

def main_menu(route_service: RouteService, network_service: NetworkService):

    while True:
        heading("ROUTECORE")
        
        print("1. Calculate Route\n")
        print("2. Add Location")
        print("3. Create Road\n")
        print("4. Change Road Status\n")
        print("5. View Locations")
        print("6. View Roads\n")
        print("7. Exit")
        
        try:
            choice = int(input("\nChoice: "))
        except ValueError:
            print("\nPlease enter a valid number.\n")
            continue
        
        if choice == 1:
            
            heading("CALCULATE ROUTE")
            
            origin = input("Origin location code: ")
            destination = input("Destination location code: ")
            try:
                route = route_service.calculate(origin, destination)
                if route is None:
                    print("\nNo route available.\n")
                    continue

                path, cost = route
                print(f"\nShortest route from {origin} to {destination}:")
                print(" -> ".join(path))
                print(f"Total distance: {cost}")
                    
            except ValueError as error:
                print(error)
                continue
        
        elif choice == 2:
            heading("Add Location")
            
            code = input("Location code (e.g. ROM): ")
            name = input("Location name (e.g. Roma): ")
            
            try:
                location = network_service.add_location(code, name)
                print(f"Location added successfully:")
                print(f"Code: {location.code}")
                print(f"Location: {location.name}")
                
            except ValueError as error:
                print(error)
        
        elif choice == 3:
            heading("Create Road")
            
            try:
                origin = input("Origin code (e.g. ROM): ")
                destination = input("Destination code (e.g. NAP): ")
                distance = float(input("Distance: "))
                status = input("Road Status (OPEN | CLOSED): ")
                
                road = network_service.add_road(origin, destination, distance, status)
                print("Road created successfully:")
                print(f"Origin: {road.origin}")
                print(f"Destination: {road.destination}")
                print(f"Length: {road.distance}")
                print(f"Status: {road.status}")
                
            except ValueError as error:
                print(error)
            
        elif choice == 4:
            heading("ROAD STATUS")
            
            try:
                origin = input("Origin Code: ")
                destination = input("Destination Code: ")
                new_status = input("New Status: ").upper().strip()
                
                if new_status == "OPEN":
                    network_service.open_road(origin, destination)
                    print(f"\nRoad status changed to {new_status}.")
                elif new_status == "CLOSED":
                    network_service.close_road(origin, destination)
                    print(f"\nRoad status changed to {new_status}.")
                else:
                    print("Not a valid status.")
                    
            except ValueError as error:
                print(error)
                    
                
        
        elif choice == 5:
            heading("LOCATIONS")
            
            locations = network_service.get_locations()
            print(f"{"CODE":<6}{"NAME":<15}")
            for location in locations:
                print(f"{location.code:<6}{location.name:<15}")
            
        
        elif choice == 6:
            heading("ROADS")
            
            roads = network_service.get_roads()
            print(f"{"ORIGIN":<8}{"DESTINATION":<13}{"DISTANCE":<10}{"STATUS"}")
            for road in roads:
                print(f"{road.origin:<8}{road.destination:<13}{road.distance:<10}{road.status}")
        
        elif choice == 7:
            break
        
        else:
            print("\nInvalid option.\n")
            
            
def heading(title: str, symbol: str = "=") -> None:
    length = len(title) + 10
    separator = symbol * length
    title = title.upper()
    
    print(f"\n{separator}\n{title.center(length)}\n{separator}\n")
    
    