# RouteCore

RouteCore is a Python project for modelling a road network and calculating routes between locations.

The project is being developed with a strong focus on software architecture, separation of responsibilities, data validation and graph algorithms.

## Current Features

- Location management
- Road management
- Bidirectional roads
- Road status management (`OPEN` / `CLOSED`)
- Duplicate location and road prevention
- JSON persistence
- Automatic storage file creation
- Atomic JSON writes using temporary files
- In-memory rollback when persistence fails
- Graph generation from the current road network
- Closed roads automatically excluded from the generated graph

## Planned Features

- Dijkstra shortest path algorithm
- Route calculation between two locations
- Delivery management
- Vehicle capacity management
- Multi-stop routes
- Command-line interface
- Automated tests

## Project Structure

```text
routecore/
├── algorithms/
│   └── dijkstra.py
│
├── models/
│   ├── location.py
│   ├── road.py
│   ├── vehicle.py
│   └── delivery.py
│
├── repositories/
│   ├── network_repository.py
│   ├── vehicle_repository.py
│   └── delivery_repository.py
│
├── services/
│   ├── network_service.py
│   ├── route_service.py
│   └── delivery_service.py
│
├── cli/
│   ├── main_menu.py
│   ├── network_menu.py
│   ├── route_menu.py
│   └── delivery_menu.py
│
├── data/
│   ├── network.json
│   ├── vehicles.json
│   └── deliveries.json
│
├── main.py
└── README.md
```

> Some modules shown above are part of the planned architecture and may not yet be implemented.

## Architecture

RouteCore separates responsibilities into different layers.

### Models

Models represent domain entities and enforce their own internal validity.

Examples:

- `Location`
- `Road`
- `Vehicle`
- `Delivery`

A `Road`, for example, validates its origin, destination, distance and status.

Models do not know how data is stored and do not contain CLI logic.

### Repositories

Repositories are responsible for persistence.

`NetworkRepository` currently handles:

- loading locations and roads from JSON;
- converting JSON data into domain objects;
- converting domain objects back into JSON;
- automatically creating the storage directory;
- automatically creating the initial network file;
- atomic writes using a temporary file;
- cleaning temporary files when persistence fails.

Repositories do not contain routing or application business logic.

### Services

Services contain application and business logic.

`NetworkService` currently handles:

- retrieving a location by code;
- retrieving a road;
- bidirectional road lookup;
- adding locations;
- adding roads;
- preventing duplicate locations;
- preventing duplicate roads;
- checking that road endpoints exist;
- opening roads;
- closing roads;
- generating the graph used by routing algorithms;
- excluding closed roads from routing;
- rolling back in-memory changes when persistence fails.

The service does not know how JSON files are written internally.

### Algorithms

Algorithms are isolated from persistence and application logic.

The planned `dijkstra.py` module will receive a graph, a starting node and a destination node and calculate the shortest available route.

The algorithm will not know about:

- JSON files;
- repositories;
- services;
- `Location` objects;
- `Road` objects;
- CLI input/output.

It will work only with the graph representation provided to it.

## Network Data Format

The network is persisted in:

```text
data/network.json
```

Example:

```json
{
    "locations": [
        {
            "name": "Roma",
            "code": "ROM"
        },
        {
            "name": "Frosinone",
            "code": "FRO"
        },
        {
            "name": "Cassino",
            "code": "CAS"
        }
    ],
    "roads": [
        {
            "origin": "ROM",
            "destination": "FRO",
            "distance": 90,
            "status": "OPEN"
        },
        {
            "origin": "FRO",
            "destination": "CAS",
            "distance": 50,
            "status": "OPEN"
        }
    ]
}
```

## Automatic Storage Initialization

When `NetworkRepository` is created, it verifies that the storage directory exists.

If necessary, the directory is created automatically.

For example:

```python
repository = NetworkRepository("./data/network.json")
```

If `data/` does not exist, it is created.

If `network.json` does not exist, RouteCore creates it with the following initial structure:

```json
{
    "locations": [],
    "roads": []
}
```

Existing network files are not overwritten during initialization.

## Locations

A location represents a node in the road network.

Example:

```python
Location(
    code="ROM",
    name="Roma"
)
```

Location codes are normalized before being stored.

For example:

```text
" rom "
```

becomes:

```text
"ROM"
```

A location validates that:

- `code` is a string;
- `code` is not empty;
- `name` is a string;
- `name` is not empty.

## Roads

A road represents a connection between two locations.

Example:

```python
Road(
    origin="ROM",
    destination="FRO",
    distance=90,
    status="OPEN"
)
```

Roads are bidirectional.

This means:

```text
ROM → FRO
```

also represents:

```text
FRO → ROM
```

A road validates that:

- `origin` is a valid non-empty string;
- `destination` is a valid non-empty string;
- origin and destination are different;
- distance is an integer or float;
- distance is greater than zero;
- status is either `OPEN` or `CLOSED`.

Road codes and status values are normalized before being stored.

## Road Status

Roads can have two states:

```text
OPEN
CLOSED
```

An open road can be used by the routing system.

A closed road still exists in the domain and in the JSON file, but it is excluded from the routing graph.

Example:

```text
A --4-- B   OPEN
B --3-- C   CLOSED
```

The generated graph will include:

```text
A ↔ B
```

but not:

```text
B ↔ C
```

Attempting to open an already open road raises an error.

Attempting to close an already closed road also raises an error.

## Graph Representation

The road network is converted into a weighted adjacency list before being passed to routing algorithms.

Example:

```python
{
    "ROM": {
        "FRO": 90
    },
    "FRO": {
        "ROM": 90,
        "CAS": 50
    },
    "CAS": {
        "FRO": 50
    }
}
```

The outer dictionary represents locations.

Each inner dictionary represents directly reachable neighbouring locations.

The value associated with each neighbour represents the road distance.

For example:

```python
graph["FRO"]["CAS"]
```

returns:

```text
50
```

## Bidirectional Graph Generation

Each open road is inserted in both directions.

A road:

```text
ROM --90-- FRO
```

produces:

```python
graph["ROM"]["FRO"] = 90
graph["FRO"]["ROM"] = 90
```

This allows routing algorithms to traverse the road in either direction.

## Isolated Locations

Locations are always represented in the graph even if they currently have no available roads.

Example:

```python
{
    "ROM": {},
    "FRO": {}
}
```

This is important because a location may exist in the network while temporarily being unreachable.

## Closed Roads

Closed roads are not included in the generated routing graph.

For example:

```text
Locations:
A
B
C

Roads:
A --4-- B   OPEN
B --3-- C   CLOSED
```

produces:

```python
{
    "A": {
        "B": 4
    },
    "B": {
        "A": 4
    },
    "C": {}
}
```

The road between `B` and `C` remains stored in the network but is unavailable to routing algorithms.

## Persistence

`NetworkRepository` converts between JSON data and domain objects.

Loading:

```text
network.json
    ↓
json.load()
    ↓
raw dictionaries
    ↓
Location / Road objects
```

Saving performs the reverse transformation:

```text
Location / Road objects
    ↓
Python dictionaries
    ↓
JSON
```

## Atomic File Writes

RouteCore avoids directly overwriting the existing network file during normal persistence.

Instead, the repository first writes the complete new state to:

```text
network.json.tmp
```

Only after the temporary file has been written successfully does RouteCore replace:

```text
network.json
```

with the temporary file.

Conceptually:

```text
current network.json
        ↓

write new data
        ↓
network.json.tmp
        ↓
write successful?
        ↓
       yes
        ↓
replace network.json atomically
```

If writing the temporary file fails:

```text
network.json
```

remains untouched.

The temporary file is removed and the original exception is propagated.

## In-Memory Rollback

Application services modify objects in memory before persistence.

If persistence fails, RouteCore restores the previous in-memory state.

For example, when adding a road:

```text
append Road
↓
attempt save
↓
save fails
↓
remove Road from memory
↓
re-raise original exception
```

When opening a road:

```text
CLOSED
↓
open()
↓
OPEN
↓
attempt save
↓
save fails
↓
close()
↓
CLOSED
```

This prevents the in-memory network from disagreeing with the persisted network after a failed save operation.

## Dependency Injection

Repositories are created outside the services and passed to them.

Example:

```python
repository = NetworkRepository("./data/network.json")

network_service = NetworkService(repository)
```

`NetworkService` does not create its own repository and does not know the path of the JSON file.

This keeps configuration separate from business logic.

Conceptually:

```text
main.py
  ↓
creates NetworkRepository
  ↓
passes repository to NetworkService
```

The same repository instance already knows its storage path.

## Separation of Responsibilities

RouteCore follows a layered structure.

```text
Model
→ represents domain data

Repository
→ reads and writes persistent data

Service
→ applies application and business rules

Algorithm
→ performs graph computation

CLI
→ handles user input and output

main.py
→ creates and connects dependencies
```

Examples:

```text
"Distance must be greater than zero"
→ Road

"Does ROM exist in the network?"
→ NetworkService

"Save network.json"
→ NetworkRepository

"Ignore CLOSED roads when building the routing graph"
→ NetworkService

"Find the shortest path"
→ algorithms/dijkstra.py

"Print the route to the terminal"
→ CLI
```

## Error Handling

RouteCore distinguishes between invalid types and invalid values.

Examples:

```text
123 instead of a string
→ TypeError
```

```text
"" as a location code
→ ValueError
```

Persistence exceptions are not silently hidden.

When a repository operation fails, the original exception is propagated after cleanup and rollback.

## Technologies and Concepts

- Python 3
- JSON
- `pathlib`
- Object-Oriented Programming
- Type hints
- Exception handling
- Dependency injection
- Repository pattern
- Service layer
- Encapsulation
- Atomic file writes
- In-memory rollback
- Weighted graphs
- Adjacency lists
- Graph algorithms

No external Python dependencies are currently required.

## Current Development Status

Implemented:

- `Location`
- `Road`
- `NetworkRepository`
- `NetworkService`
- JSON persistence
- automatic storage initialization
- atomic saves
- rollback logic
- road opening and closing
- duplicate prevention
- graph generation

In development:

- Dijkstra shortest-path algorithm

Planned:

- `RouteService`
- delivery management
- vehicle management
- vehicle capacity validation
- multi-stop routes
- CLI
- automated tests

## Next Milestone

The next major milestone is the implementation of Dijkstra's shortest-path algorithm.

The algorithm will operate on a graph such as:

```python
{
    "A": {
        "B": 4,
        "C": 8
    },
    "B": {
        "A": 4,
        "C": 3,
        "D": 7
    },
    "C": {
        "A": 8,
        "B": 3,
        "D": 2
    },
    "D": {
        "B": 7,
        "C": 2
    }
}
```

For example:

```text
Start: A
Destination: D
```

the routing system should eventually determine:

```text
A → B → C → D
```

with total distance:

```text
9
```

## Project Goal

RouteCore is primarily a learning project designed to strengthen:

- Python programming;
- software architecture;
- problem decomposition;
- object-oriented design;
- data structures;
- graph theory;
- algorithms;
- persistence;
- error handling;
- backend development fundamentals.

The goal is not only to make the application work, but to understand why each responsibility belongs where it does and how the different layers interact.