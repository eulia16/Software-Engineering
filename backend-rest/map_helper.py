import data_models
import database_handler


def update_robot(map_id, robot_position, direction,
                 password, host="localhost", port=5432, database="RobotRadarAlpha"):
    candidates = data_models.MapObject.get_map_objects(
        password=password,
        map_id=map_id,
        object_type="OurRobot",
        host=host,
        port=port,
        database=database
    )

    if len(candidates) > 0:
        our_robot = candidates[0]
        our_robot.location = robot_position
        our_robot.direction = direction
        our_robot.update_map_object_location(password=password, host=host, port=port, database=database)
    else:
        our_robot = data_models.MapObject(map_id=map_id, location_x=robot_position[0], location_y=robot_position[1],
                                          object_type="OurRobot", direction=direction)
        our_robot.create(password=password, host=host, port=port, database=database)


def update_other_robot(map_id, robot_position, direction,
                       password, host="localhost", port=5432, database="RobotRadarAlpha"):
    candidates = data_models.MapObject.get_map_objects(
        password=password,
        map_id=map_id,
        object_type="OtherRobot",
        host=host,
        port=port,
        database=database
    )

    if len(candidates) > 0:
        other_robot = candidates[0]
        other_robot.location = robot_position
        other_robot.direction = direction
        other_robot.update_map_object_location(password=password, host=host, port=port, database=database)
    else:
        other_robot = data_models.MapObject(map_id=map_id, location_x=robot_position[0], location_y=robot_position[1],
                                            object_type="OtherRobot", direction=direction)
        other_robot.create(password=password, host=host, port=port, database=database)


# Takes a radar reading, sees if any obstacles or the other robot in the database matches
# the position of the calculated obstacle coordinates and if so, creates a new obstacle entry and returns true.
# Otherwise, it returns False.
def obstacle_detection(map_id, robot_position, radar_reading, direction,
                       password, host="localhost", port=5432, database="RobotRadarAlpha"):
    if radar_reading > 35:
        return False

    potential_obstacle_coordinates = \
        convert_radar_coordinates(robot_position=robot_position, radar_reading=radar_reading, direction=direction)

    p_obst_x = potential_obstacle_coordinates[0]
    p_obst_y = potential_obstacle_coordinates[1]

    map_objects = data_models.MapObject.get_map_objects(
        password=password,
        map_id=map_id,
        host=host,
        port=port,
        database=database
    )

    found_match = False

    for map_object in map_objects:
        obj_x = map_object.location[0]
        obj_y = map_object.location[1]

        if obj_x == p_obst_x and obj_y == p_obst_y:
            found_match = True
            # Got what we needed
            break

    if not found_match:
        new_obstacle = data_models.MapObject(map_id=map_id, object_type="Can",
                                             location_x=p_obst_x, location_y=p_obst_y)
        new_obstacle.create(password=password, host=host, port=port, database=database)

        return True
    else:
        return False


# We get our position in meters, need to convert to blocks for the map.
# Blocks are 50cm each.
def convert_robot_position(raw_robot_position, block_size=50):
    raw_robot_x = raw_robot_position[0]
    raw_robot_y = raw_robot_position[1]

    new_robot_x = round((raw_robot_x * 100) / block_size)
    new_robot_y = round((raw_robot_y * 100) / block_size)

    robot_position = (new_robot_x, new_robot_y)

    return robot_position


# Radar reading comes in cm, convert to blocks
def __convert_radar_reading(radar_reading, block_size=50):
    candidate_value = round(radar_reading / block_size)

    if candidate_value == 0:
        return 1

    return candidate_value


# robot_position needs to be converted to blocks first
def convert_radar_coordinates(direction, robot_position, radar_reading):
    radar_blocks = __convert_radar_reading(radar_reading=radar_reading)

    # This is to make sure we don't have any pass by reference funny business going on
    detected_position = robot_position + tuple()

    if direction == "W":
        detected_position = (detected_position[0] - radar_blocks, detected_position[1])
    elif direction == "E":
        detected_position = (detected_position[0] + radar_blocks, detected_position[1])
    elif direction == "N":
        detected_position = (detected_position[0], detected_position[1] + radar_blocks)
    else:
        detected_position = (detected_position[0], detected_position[1] - radar_blocks)

    return detected_position


def convert_dijkstra_to_moves(dijkstra_coordinates, robot_record):
    # Start variables: Where the robot is right now, aka where it is starting
    # Current variables: keep track of position when building move list

    # Received coordinates already have current position - start from first in the list
    current_pos = dijkstra_coordinates.pop(0)

    current_dir = robot_record.direction

    coordinates = dijkstra_coordinates
    move_list = []

    for coordinate in coordinates:
        # X and Y are swapped on the frontend
        current_x = current_pos[1]
        current_y = current_pos[0]

        next_x = coordinate[1]
        next_y = coordinate[0]

        # Turn to face east
        if next_x > current_x:
            if current_dir == "N":
                move_list.append("r")
                current_dir = "E"
            elif current_dir == "W":
                move_list.extend(["r", "r"])
                current_dir = "E"
            elif current_dir == "S":
                move_list.append("l")
                current_dir = "E"

        # Turn to face west
        elif next_x < current_x:
            if current_dir == "N":
                move_list.append("l")
                current_dir = "W"
            elif current_dir == "E":
                move_list.extend(["l", "l"])
                current_dir = "W"
            elif current_dir == "S":
                move_list.append("r")
                current_dir = "W"

        # Turn to face north
        elif next_y > current_y:
            if current_dir == "E":
                move_list.append("l")
                current_dir = "N"

            elif current_dir == "S":
                move_list.extend(["l", "l"])
                current_dir = "N"

            elif current_dir == "W":
                move_list.append("r")
                current_dir = "N"

        # Turn to face south
        elif next_y < current_y:
            if current_dir == "E":
                move_list.append("r")
                current_dir = "S"

            elif current_dir == "N":
                move_list.extend(["l", "l"])
                current_dir = "S"

            elif current_dir == "W":
                move_list.append("l")
                current_dir = "S"

        move_list.append("f")
        current_pos = coordinate

    return move_list
