# Backend Rest

## Creating Docker Image and Testing Locally
Make sure you have Docker installed!

To get testing:
1. Run `docker build -t flask-app-backend . `
2. Run `docker run -p 9823:5000 -d flask-app-backend`
3. Hit `http://localhost:9823/logs?password=<password>&istest=False` in either Postman or your
browser.  If it works, everything built correctly!

## API Specification

### /initialize

#### GET
For the robot to hit so its public IP can be stored in the `robot_ip` session
variable.

- Returns
  - `Got IP` (string value)
- URL Parameters
  - None

### /checkip

#### GET
Returns the IP of the robot stored in the session, if available.

- Returns
  - Stored robot public IP as a string
  - Empty string if unavailable
- URL Parameters
  - None


### /generatepano

Tells the robot to take a panoramic view.  Images are received as a `.zip`,
are unzipped into `panoramic-images/received-data/...` and then the images are copied out of 
the received file structure into the root of `panoramic-images`.

#### GET

- Returns
  - `Panoramic pictures taken and saved` (string)
- URL Parameters
  - None


### /panoramic

Get a stitched together panoramic of pictures the robot takes
facing North, South, East and West.  If there are no pictures to stitch, a black 
square picture is returned.

#### GET
- Returns
  - Image of type `.png`
- URL Parameters
  - None

### /current_view

Get the latest image saved from the robot's PoV.  If there are no pictures to stitch, a black 
square picture is returned.

#### GET
- Returns
  - Image of type `.png`
- URL Parameters
  - None



#### GET
- Returns
  - Image of type `.png`
- URL Parameters
  - None


### /clear_obstacles

#### GET

Deletes all obstacles for the given map id.  Returns what remains for that map -
should be the robot record plus the ghost obstacle with matching coordinates.

- Returns
  - JSON object of a list of MapObjects
  - Sample JSON:
  ```json
  [
      {
          "map_id": 1,
          "object_type": "Can",
          "location": [
              5,
              5
          ],
          "created_at": "2022-11-12T00:43:29.532003",
          "direction": null,
          "obj_id": 1
      },
      {
          "map_id": 1,
          "object_type": "OurRobot",
          "location": [
              5,
              5
          ],
          "created_at": "2022-11-12T00:43:29.532003",
          "direction": "E",
          "obj_id": 1
      }
  ]
  ```
- URL Parameters
  - *objtype*
    - The type of MapObject to be returned.  Valid values are
    `Can`, `OtherRobot` and `OurRobot`
  - *istest*
    - If this is a local endpoint meant to use a local 
    Docker database (`True` or `False`). Optional, defaults to `False`
  - *password*
    - Password for `flaskuser`.
  - *remote*
    - Connect to the Docker DB on remote (`True` or `False`).  
    Optional, defaults to `False`.


### /mapdata

#### GET

- Returns
  - JSON object of a list of MapObjects
  - Sample JSON:
  ```json
  [
      {
          "map_id": 1,
          "object_type": "Can",
          "location": [
              7,
              4
          ],
          "created_at": "2022-11-12T01:13:27.631719",
          "direction": null,
          "obj_id": 3
      },
      {
          "map_id": 1,
          "object_type": "Can",
          "location": [
              5,
              5
          ],
          "created_at": "2022-11-12T00:43:29.532003",
          "direction": null,
          "obj_id": 1
      },
      {
          "map_id": 1,
          "object_type": "OurRobot",
          "location": [
              5,
              5
          ],
          "created_at": "2022-11-12T00:43:29.532003",
          "direction": "E",
          "obj_id": 1
      }
  ]
  ```
- URL Parameters
  - *mapid*
    - Id of the Map the returned objects are associated with.
  - *objtype*
    - The type of MapObject to be returned.  Valid values are
    `Can`, `OtherRobot` and `OurRobot`
  - *istest*
    - If this is a local endpoint meant to use a local 
    Docker database (`True` or `False`). Optional, defaults to `False`
  - *password*
    - Password for `flaskuser`.
  - *remote*
    - Connect to the Docker DB on remote (`True` or `False`).  
    Optional, defaults to `False`.

#### POST
Creates a new Map and sets its id to the session variable `current_map_id`.
- Returns
  - `New Map ID: <Map Id>`
- URL Parameters
  - None

### /move

#### GET
Moves the robot in the specified direction, updates its location as well as 
saves any new obstacles detected.  Will include a "ghost" obstacle whose coordinates match the robot's

- Returns
  - JSON object of a list of MapObjects
  - Sample JSON:
  ```json
  [
      {
          "map_id": 1,
          "object_type": "Can",
          "location": [
              7,
              4
          ],
          "created_at": "2022-11-12T01:13:27.631719",
          "direction": null,
          "obj_id": 3
      },
      {
          "map_id": 1,
          "object_type": "Can",
          "location": [
              5,
              5
          ],
          "created_at": "2022-11-12T00:43:29.532003",
          "direction": null,
          "obj_id": 1
      },
      {
          "map_id": 1,
          "object_type": "OurRobot",
          "location": [
              5,
              5
          ],
          "created_at": "2022-11-12T00:43:29.532003",
          "direction": "E",
          "obj_id": 1
      }
  ]
  ```
- URL Parameters
  - *movekey*
    - Key pressed for movement.  Valid values are `W` (move forward), `A` (turn left),
    `S` (move backward) or `D` (turn right).  
  - *istest*
    - If this is a local endpoint meant to use a local 
    Docker database (`True` or `False`). Optional, defaults to `False`
  - *password*
    - Password for `flaskuser`.
  - *remote*
    - Connect to the Docker DB on remote (`True` or `False`).  
    Optional, defaults to `False`.

### /testrobotconnect

#### GET
Checks to see if the robot is reachable by sending a request to its
`/coffee` endpoint.

- Returns
  - Success:
    - `Test connect to robot successful!` (string)
  - Failure:
    - `Could not reach robot.` (string)
- URL Parameters
  - None

### /logs

#### GET
Returns a list of JSON-formatted logs from the database.

- Returns
  - Success (sample JSON):
  ```json
  [
    {
        "created_at": "2022-11-04T14:05:32.478150",
        "origin": "app.py",
        "message": "invalid integer value \"localhost\" for connection option \"port\"\n",
        "log_type": "Error",
        "stack_trace": "",
        "id": 10
    },
    {
        "created_at": "2022-11-04T14:07:12.071802",
        "origin": "app.py",
        "message": "Logs retrieved from /logs GET",
        "log_type": "Event",
        "stack_trace": "",
        "id": 11
    }
  ]
  ```
  - Failure:
    - `An error occurred - see logs` (string)
- URL Parameters
  - *istest*
    - If this is a local endpoint meant to use a local 
    Docker database (`True` or `False`). Optional, defaults to `False`
  - *password*
    - Password for `flaskuser`.
  - *remote*
    - Connect to the Docker DB on remote (`True` or `False`).  
    Optional, defaults to `False`.


### /autonomous

#### POST
Receives a set of Dijkstra-calculated coordinates to be translated into movements
to send to the robot.  Will return the current map objects, including a "ghost" obstacle
whose coordinates match the robot's.  This ghost is required for the frontend to execute its Dijkstra command.

- Request Body Structure 
  ```json
    {
       "Coordinates":
        [
           [15, 1],
           [15, 2],
           [15, 3],
           [15, 4],
           [15, 5],
           [15, 6],
           [15, 7],
           [15, 8],
           [15, 9]
       ]
    }
  ```
- Returns
  - JSON object of a list of MapObjects
  - Sample JSON:
  ```json
  [
      {
          "map_id": 1,
          "object_type": "Can",
          "location": [
              7,
              4
          ],
          "created_at": "2022-11-12T01:13:27.631719",
          "direction": null,
          "obj_id": 3
      },
      {
          "map_id": 1,
          "object_type": "Can",
          "location": [
              5,
              5
          ],
          "created_at": "2022-11-12T00:43:29.532003",
          "direction": null,
          "obj_id": 1
      },
      {
          "map_id": 1,
          "object_type": "OurRobot",
          "location": [
              5,
              5
          ],
          "created_at": "2022-11-12T00:43:29.532003",
          "direction": "E",
          "obj_id": 1
      }
  ]
  ```
- URL Parameters
  - *istest*
    - If this is a local endpoint meant to use a local 
    Docker database (`True` or `False`). Optional, defaults to `False`
  - *password*
    - Password for `flaskuser`.
  - *remote*
    - Connect to the Docker DB on remote (`True` or `False`).  
    Optional, defaults to `False`.


### /move

#### GET
Moves the robot in the specified direction, updates its location as well as 
saves any new obstacles detected.

- Returns
  - JSON object of a list of MapObjects
  - Sample JSON:
  ```json
  [
      {
          "map_id": 1,
          "object_type": "Can",
          "location": [
              31,
              25
          ],
          "created_at": "2022-11-12T01:13:27.631719",
          "direction": null,
          "obj_id": 3
      },
      {
          "map_id": 1,
          "object_type": "OurRobot",
          "location": [
              26,
              25
          ],
          "created_at": "2022-11-12T00:43:29.532003",
          "direction": "E",
          "obj_id": 1
      }
  ]
  ```
- URL Parameters
  - *movekey*
    - Key pressed for movement.  Valid values are `W` (move forward), `A` (turn left),
    `S` (move backward) or `D` (turn right).  
  - *istest*
    - If this is a local endpoint meant to use a local 
    Docker database (`True` or `False`). Optional, defaults to `False`
  - *password*
    - Password for `flaskuser`.
  - *remote*
    - Connect to the Docker DB on remote (`True` or `False`).  
    Optional, defaults to `False`.

### /other_robot

#### POST
Endpoint for the other robot team to send their updated position and current radar reading to.

- Request Body Structure 
  ```json
  {
      "location": [
          3,
          2
      ],
      "orientation": "E",
      "radar": 48
  }
  ```
    - `location` should have both coordinate values in meters
    - `radar` is measured in centimeters
- Returns
  - JSON object of a list of MapObjects
  - Sample JSON:
  ```json
  [
    {
        "map_id": 1,
        "object_type": "OurRobot",
        "location": [
            14,
            1
        ],
        "created_at": "2022-11-12T00:43:29.532003",
        "direction": "E",
        "obj_id": 1
    },
    {
        "map_id": 1,
        "object_type": "Can",
        "location": [
            35,
            20
        ],
        "created_at": "2022-11-15T19:31:31.705408",
        "direction": null,
        "obj_id": 10
    },
    {
        "map_id": 1,
        "object_type": "OtherRobot",
        "location": [
            30,
            20
        ],
        "created_at": "2022-11-15T19:31:31.643092",
        "direction": "E",
        "obj_id": 9
    }
  ]
  ```
- URL Parameters
  - *istest*
    - If this is a local endpoint meant to use a local 
    Docker database (`True` or `False`). Optional, defaults to `False`
  - *password*
    - Password for `flaskuser`.
  - *remote*
    - Connect to the Docker DB on remote (`True` or `False`).  
    Optional, defaults to `False`.