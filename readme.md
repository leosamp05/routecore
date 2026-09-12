# RouteCore

RouteCore is a Python command-line application for managing a small road network and calculating the shortest available route between locations.

The project is built with a layered architecture that separates domain models, persistence, business logic, routing algorithms, and the CLI.

## Features

- Add locations
- Create bidirectional roads between locations
- Set roads as `OPEN` or `CLOSED`
- Change the status of an existing road
- View all locations
- View all roads with distance and status
- Calculate the shortest route between two locations
- Automatically ignore closed roads during route calculation
- Detect unreachable destinations
- Persist network data in JSON
- Restore saved data when the application starts
- Prevent duplicate locations
- Prevent duplicate roads, including reversed duplicates
- Validate location, road, distance, and status data

## Shortest Path

RouteCore uses Dijkstra's algorithm to calculate the shortest available route between two locations.

Only roads with status:

```text
OPEN
```

are included in the graph used by the algorithm.

Example network:

```text
ROM ----90---- FRO
 |              |
300             80
 |              |
 +----- NAP ----+
```

Calculating:

```text
ROM -> NAP
```

returns:

```text
ROM -> FRO -> NAP
Total distance: 170
```

instead of the direct road with distance `300`.

If no valid route exists, the application reports:

```text
No route available.
```

## Road Status

Roads can have one of two statuses:

```text
OPEN
CLOSED
```

Closed roads remain stored in the network but are excluded when building the graph used by Dijkstra's algorithm.

Changing a road from `CLOSED` back to `OPEN` makes it immediately available for route calculation again.

## Data Persistence

Network data is stored in:

```text
data/network.json
```

The file contains locations and roads.

Example:

```json
{
    "locations": [
        {
            "name": "Rome",
            "code": "ROM"
        },
        {
            "name": "Frosinone",
            "code": "FRO"
        }
    ],
    "roads": [
        {
            "origin": "ROM",
            "destination": "FRO",
            "distance": 90,
            "status": "OPEN"
        }
    ]
}
```

Changes are automatically saved.

The repository writes the updated data to a temporary file before replacing the existing network file, reducing the risk of corrupting the current data during a save operation.

## Project Structure

```text
routecore/
├── algorithms/
│   └── dijkstra.py
│
├── cli/
│   └── main_menu.py
│
├── data/
│   └── network.json
│
├── models/
│   ├── location.py
│   └── road.py
│
├── repositories/
│   └── network_repository.py
│
├── services/
│   ├── network_service.py
│   └── route_service.py
│
├── main.py
└── README.md
```

## Architecture

The application follows a layered structure:

```text
CLI
 ↓
Services
 ↓
Algorithms / Repositories
 ↓
Models / JSON data
```

### Models

Domain entities and their validation rules.

#### `Location`

Represents a location in the network.

Main data:

```text
code
name
```

Location codes are normalized to uppercase.

#### `Road`

Represents a bidirectional connection between two locations.

Main data:

```text
origin
destination
distance
status
```

A road:

- cannot connect a location to itself
- must have a positive distance
- must have status `OPEN` or `CLOSED`

The model also manages its own status transitions through open and close operations.

## Repository

### `NetworkRepository`

Responsible for JSON persistence.

It:

- creates the data directory when necessary
- creates an empty network file if none exists
- loads locations and roads from JSON
- converts JSON data into domain objects
- converts domain objects back into JSON
- saves network changes

File access is kept outside the services and CLI.

## Services

### `NetworkService`

Manages the road network.

Responsibilities include:

- retrieving locations
- retrieving roads
- adding locations
- adding roads
- opening roads
- closing roads
- preventing duplicate locations
- preventing duplicate bidirectional roads
- validating that road endpoints exist
- saving network changes
- building the graph used for route calculation

The graph contains all locations but only roads currently marked as `OPEN`.

### `RouteService`

Coordinates route calculation.

It:

1. validates the origin location
2. validates the destination location
3. requests the current graph from `NetworkService`
4. calls Dijkstra's algorithm
5. returns the calculated path and total distance

The service returns:

```python
tuple[list[str], int | float] | None
```

Example:

```python
(["ROM", "FRO", "NAP"], 170.0)
```

If the destination cannot be reached:

```python
None
```

## Dijkstra Algorithm

The routing algorithm is implemented separately in:

```text
algorithms/dijkstra.py
```

It receives:

```python
graph
origin
destination
```

and returns the shortest route and its total cost.

Example:

```python
(["ROM", "FRO", "NAP"], 170.0)
```

The algorithm keeps track of:

- the lowest known cost for every node
- the previous node in the best known path
- nodes that still need to be explored

The final route is reconstructed by following the previous nodes from the destination back to the origin.

## CLI

The command-line interface currently provides:

```text
1. Calculate Route

2. Add Location
3. Create Road

4. Change Road Status

5. View Locations
6. View Roads

7. Exit
```

### Calculate Route

Example:

```text
Origin location code: rom
Destination location code: nap

Shortest route from rom to nap:
ROM -> FRO -> NAP
Total distance: 170.0
```

### View Locations

Example:

```text
CODE  NAME
ROM   Rome
FRO   Frosinone
NAP   Naples
```

### View Roads

Example:

```text
ORIGIN  DESTINATION  DISTANCE  STATUS
ROM     FRO          90.0      OPEN
FRO     NAP          80.0      OPEN
ROM     NAP          300.0     OPEN
```

## Validation

RouteCore currently validates several invalid states.

Examples include:

### Duplicate location

```text
Location already exists.
```

Location codes are normalized, so:

```text
rom
ROM
```

refer to the same location.

### Duplicate road

Because roads are bidirectional, if this road exists:

```text
ROM -> FRO
```

trying to create:

```text
FRO -> ROM
```

is rejected.

```text
Road already exists.
```

### Missing location

A road cannot be created if one of its endpoints does not exist.

Example:

```text
Destination does not exist.
```

### Invalid distance

Road distances must be greater than zero.

```text
Distance must be positive.
```

### Invalid status

Only these values are accepted:

```text
OPEN
CLOSED
```

## Running the Project

Requirements:

```text
Python 3.10+
```

No external Python packages are currently required.

Run the application from the project root:

```bash
python main.py
```

## Entry Point

`main.py` creates and connects the application dependencies:

```text
NetworkRepository
        ↓
NetworkService
        ↓
RouteService
        ↓
CLI
```

This keeps object creation centralized and avoids coupling services directly to the application's entry point.

## Current Status

The current version implements the complete basic location, road-network, persistence, CLI, and shortest-route workflow.