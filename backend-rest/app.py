# Referred to: https://www.geeksforgeeks.org/python-build-a-rest-api-using-flask/?id=discuss
# { DEV }	-	{ YYYY/MM/DD }	-	{ MODIFICATIONS }
# vlock     -     2022/10/30    -   Added base panoramic image functionality
# vlock     -     2022/11/07    -   (Previous updates not recorded) Further cleanup and documentation
# import necessary libraries and functions
import io
import json
import os
import zipfile
import shutil
import requests

from flask import Flask, request, send_file, session

from flask_session import Session
from flask_cors import CORS
from PIL import Image
from os.path import exists

import database_handler
import data_models
import map_helper

# creating a Flask app
app = Flask(__name__)
CORS(app)

# Setup session info
SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
Session(app)


# When the robot hits this, it will save the public IP to the current session.
@app.route('/initialize', methods=['GET'])
def initialize_robot_ip():
    session["robot_ip"] = "http://" + request.remote_addr + ":5000"

    print(request.remote_addr + ":5000")
    return "Got IP"


# Gets the saved public IP of the robot for the current session.
# Returns an empty string if not available.
@app.route('/checkip', methods=['GET'])
def check_ip():
    if "robot_ip" in session:
        return str(session["robot_ip"])
    else:
        return ""


def __get_robot_ip():
    if "robot_ip" in session:
        return str(session["robot_ip"])
    else:
        return "<ENTER IP HERE>"  # Put the public IP that reaches the pi here


def __get_current_map_id():
    if "robot_ip" in session:
        return int(session["current_map_id"])
    else:
        return 1


def __get_current_direction():
    if "current_direction" in session:
        return str(session["current_direction"])
    else:
        return "E"


# Referred to this tutorial:
# https://www.tutorialspoint.com/python_pillow/Python_pillow_merging_images.htm
# Sends a request to the robot for pictures, then stitches the received pictures together into a panorama
# URL PARAMS:
# - istest      -   If this is a local endpoint meant to use a local Docker database (True or False).
# - password    -   Password for flaskuser.
# - remote       -   Connect to the Docker DB on remote (True or False).
@app.route('/panoramic', methods=['GET'])
def panoramic():
    image1_url = 'panoramic-images/frontPicture.png'
    file1_exists = exists(image1_url)

    image2_url = 'panoramic-images/ninetyDegreesPicture.png'
    file2_exists = exists(image2_url)

    image3_url = 'panoramic-images/oneEightyDegreesPicture.png'
    file3_exists = exists(image3_url)

    image4_url = 'panoramic-images/twoSeventyDegreesPicture.png'
    file4_exists = exists(image4_url)

    if not (file1_exists and file2_exists and file3_exists and file4_exists):
        empty_image_fp = 'panoramic-images/empty-image.png'
        empty_image = Image.new('RGB', (500, 500))
        empty_image.save(empty_image_fp)

        response = send_file(empty_image_fp, mimetype="image/png")
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

    # Get each directional image from the robot
    panel_north = Image.open(image1_url)
    panel_east = Image.open(image2_url)
    panel_south = Image.open(image3_url)
    panel_west = Image.open(image4_url)

    # We'll load these into a list so if we for some reason add more panels
    # we only have a couple places to modify
    panel_list = [panel_north, panel_east, panel_south, panel_west]

    # Defer to the first panel for dimensions
    panel_width = panel_list[0].size[0]
    panel_height = panel_list[0].size[1]

    # Resize each panel if dimensions don't match
    processed_panels = []

    for panel in panel_list:
        processed_panel = panel
        if panel.size[0] != panel_width or panel.size[1] != panel_height:
            processed_panel = panel.resize((panel_width, panel_height))
        processed_panels.append(processed_panel)

    num_panels = len(processed_panels)

    # Instantiate the panoramic image
    panoramic_image = Image.new('RGB', (num_panels * panel_width, panel_height))

    # Stitch the panels together for the full image
    for panel_position in range(num_panels):
        stitch_position = panel_position * panel_width
        panoramic_image.paste(processed_panels[panel_position], (stitch_position, 0))

    # Save the new image
    pano_filepath = "panoramic-images/full-pano.png"
    panoramic_image.save(pano_filepath)

    # Send the image home!
    response = send_file(pano_filepath, mimetype="image/png")
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/generatepano', methods=['GET'])
def generate_panoramic():
    karr_ip = __get_robot_ip()
    api_url = karr_ip + "/camera"

    api_response = requests.get(api_url)
    received_zip = zipfile.ZipFile(io.BytesIO(api_response.content))
    received_zip.extractall("panoramic-images/received-data")

    src_dir = "panoramic-images/received-data/home/pi/Desktop/pictures"
    dest_dir = "panoramic-images"

    # Test data
    # with zipfile.ZipFile("sample-data/data.zip", "r") as zip_ref:
    #    zip_ref.extractall("panoramic-images/received-data")

    files = os.listdir(src_dir)

    for grabbed_file in files:
        shutil.copy2(os.path.join(src_dir, grabbed_file), dest_dir)

    response = Flask.response_class()
    response.data = "Panoramic pictures taken and saved"
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


# Shows the most recently taken photo by the robot
@app.route('/current_view', methods=['GET'])
def get_current_view():
    # Only uncomment this for testing
    # update_current_camera_view()
    picture_fp = 'panoramic-images/camera-data/liveStream.png'
    file_exists = exists(picture_fp)

    if file_exists:
        response = send_file(picture_fp, mimetype="image/png")
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    else:
        empty_image_fp = 'panoramic-images/empty-image.png'
        empty_image = Image.new('RGB', (500, 500))
        empty_image.save(empty_image_fp)

        response = send_file(empty_image_fp, mimetype="image/png")
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response


# Returns formatted map data.
# URL PARAMS (GET):
# - istest      -   If this is a local endpoint meant to use a local Docker database (True or False).
# - password    -   Password for flaskuser.
# - remote       -   Connect to the Docker DB on remote (True or False).
@app.route('/mapdata', methods=['GET', 'POST'])
def mapdata():
    connection_info = database_handler.get_connection_info(request)

    password = connection_info[0]
    host = connection_info[1]
    call_port = connection_info[2]

    map_id = request.args.get("mapid")

    if map_id is None:
        map_id = __get_current_map_id()

    object_type = request.args.get("objtype")

    if request.method == 'GET':
        response = Flask.response_class()
        response.content_type = "json"

        data = data_models.MapObject.get_map_objects(map_id=map_id, object_type=object_type, password=password,
                                                     host=host, port=call_port)

        # Dijkstra apparently needs this to work
        ghost_candidates = data_models.MapObject.get_map_objects(map_id=map_id, password=password,
                                                                 host=host, port=call_port, object_type="OurRobot")
        ghost = ghost_candidates[0]
        ghost.object_type = "Can"
        ghost.direction = None

        data.append(ghost)

        response.data = json.dumps(data, cls=data_models.DataModelJsonEncoder)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    else:
        new_map = data_models.Map.create(password=password, host=host, port=call_port)

        session["current_map_id"] = new_map.id

        response = Flask.response_class()
        response.status_code = 201
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.data = "New Map ID: %s" % new_map.id
        return response


@app.route('/other_robot', methods=['POST'])
def other_robot():
    other_robot_json = request.json
    connection_info = database_handler.get_connection_info(request)
    password = connection_info[0]
    host = connection_info[1]
    call_port = connection_info[2]

    response = Flask.response_class()
    response.headers.add('Access-Control-Allow-Origin', '*')

    map_id = __get_current_map_id()

    process_other_robot_request(robot_response=other_robot_json, map_id=map_id,
                                password=password, host=host, call_port=call_port)

    data = data_models.MapObject.get_map_objects(map_id=map_id, password=password,
                                                 host=host, port=call_port)

    response.data = json.dumps(data, cls=data_models.DataModelJsonEncoder)
    response.content_type = "json"

    return response


# Deletes all obstacles associated with the current map
# URL PARAMS:
# - istest      -   If this is a local endpoint meant to use a local Docker database (True or False).
# - password    -   Password for flaskuser.
# - remote       -   Connect to the Docker DB on remote (True or False).
@app.route('/clear_obstacles', methods=['GET'])
def clear_obstacles():
    connection_info = database_handler.get_connection_info(request)

    password = connection_info[0]
    host = connection_info[1]
    call_port = connection_info[2]

    map_id = __get_current_map_id()

    try:
        data_models.MapObject.delete_obstacles(password=password, map_id=map_id, host=host, port=call_port)

        response = Flask.response_class()
        response.content_type = "json"

        data = data_models.MapObject.get_map_objects(map_id=map_id, object_type=None, password=password,
                                                     host=host, port=call_port)

        # Dijkstra apparently needs this to work
        ghost_candidates = data_models.MapObject.get_map_objects(map_id=map_id, password=password,
                                                                 host=host, port=call_port, object_type="OurRobot")
        ghost = ghost_candidates[0]
        ghost.object_type = "Can"
        ghost.direction = None

        data.append(ghost)

        response.data = json.dumps(data, cls=data_models.DataModelJsonEncoder)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    except Exception as ex:
        exception_message = get_exception_message(ex)

        error_log = data_models.Log(origin=os.path.basename(__file__), message=exception_message, log_type="Error")
        error_log.create(password=password, host=host, port=call_port)

        response = Flask.response_class()

        response.data = "An error occurred - see logs"
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response


# Retrieves logs from the DB.
# URL PARAMS:
# - istest      -   If this is a local endpoint meant to use a local Docker database (True or False).
# - password    -   Password for flaskuser.
# - remote       -   Connect to the Docker DB on remote (True or False).
@app.route('/logs', methods=['GET', 'POST'])
def logs():
    connection_info = database_handler.get_connection_info(request)

    password = connection_info[0]
    host = connection_info[1]
    call_port = connection_info[2]

    try:
        if request.method == 'GET':
            response = Flask.response_class()
            response.content_type = "json"

            data = data_models.Log.get_latest_logs(password=password, host=host, port=call_port)
            response.data = json.dumps(data, cls=data_models.DataModelJsonEncoder)

            response.status_code = 200
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response
    except Exception as ex:
        exception_message = get_exception_message(ex)

        error_log = data_models.Log(origin=os.path.basename(__file__), message=exception_message, log_type="Error")
        error_log.create(password=password, host=host, port=call_port)

        response = Flask.response_class()

        response.data = "An error occurred - see logs"
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response


# Takes formatted coordinate request and converts them to move commands for the robot.
# URL PARAMS:
# - istest      -   If this is a local endpoint meant to use a local Docker database (True or False).
# - password    -   Password for flaskuser.
# - remote       -   Connect to the Docker DB on remote (True or False).
@app.route('/autonomous', methods=['POST'])
def autonomous():
    dijkstra_coordinates = request.json

    connection_info = database_handler.get_connection_info(request)
    password = connection_info[0]
    host = connection_info[1]
    call_port = connection_info[2]

    logged_coordinates = data_models.Log(origin=os.path.basename(__file__), message=json.dumps(dijkstra_coordinates),
                                         log_type="Event")
    logged_coordinates.create(password=password, host=host, port=call_port)

    delimiter = ','

    karr_ip = __get_robot_ip()
    api_url = karr_ip + "/autonomous/"

    response = Flask.response_class()
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add("Access-Control-Allow-Methods", "POST")

    map_id = __get_current_map_id()

    move_list = process_autonomous_request(map_id=map_id, dijkstra_coordinates=dijkstra_coordinates,
                                           password=password, host=host, call_port=call_port)

    api_url = api_url + delimiter.join(move_list)
    robot_response = requests.get(api_url).json()

    process_robot_response(robot_response=robot_response, map_id=map_id,
                           password=password, host=host, call_port=call_port)

    data = data_models.MapObject.get_map_objects(map_id=map_id, password=password,
                                                 host=host, port=call_port)

    # Dijkstra apparently needs this to work
    ghost_candidates = data_models.MapObject.get_map_objects(map_id=map_id, password=password,
                                                             host=host, port=call_port, object_type="OurRobot")
    ghost = ghost_candidates[0]
    ghost.object_type = "Can"
    ghost.direction = None

    data.append(ghost)

    response.data = json.dumps(data, cls=data_models.DataModelJsonEncoder)
    response.content_type = "json"

    return response


# Takes a move character and sends the corresponding move command to the robot.
# URL PARAMS:
# - istest      -   If this is a local endpoint meant to use a local Docker database (True or False).
# - password    -   Password for flaskuser.
# - remote       -   Connect to the Docker DB on remote (True or False).
# - movekey     -   The movement keyboard key hit (W, A, S or D).
@app.route('/move', methods=['GET'])
def move():
    connection_info = database_handler.get_connection_info(request)

    password = connection_info[0]
    host = connection_info[1]
    call_port = connection_info[2]

    move_key = request.args.get("movekey")

    response = Flask.response_class()
    response.headers.add('Access-Control-Allow-Origin', '*')

    map_id = __get_current_map_id()

    karr_ip = __get_robot_ip()
    robot_response = None

    '''
    obstacles_in_way = check_if_obstacles_in_the_way(map_id=map_id, password=password, host=host, call_port=call_port)

    if obstacles_in_way:
        data = data_models.MapObject.get_map_objects(map_id=map_id, password=password,
                                                     host=host, port=call_port)

        response.data = json.dumps(data, cls=data_models.DataModelJsonEncoder)
        response.content_type = "json"

        return response
    '''

    # Position is returned from robot in meters
    try:
        match move_key:
            case "W":
                api_url = karr_ip + "/forward"
                robot_response = requests.get(api_url).json()
            case "S":
                api_url = karr_ip + "/backward"
                robot_response = requests.get(api_url).json()
            case "A":
                api_url = karr_ip + "/left"
                robot_response = requests.get(api_url).json()
            case "D":
                api_url = karr_ip + "/right"
                robot_response = requests.get(api_url).json()

        process_robot_response(robot_response=robot_response, map_id=map_id,
                               password=password, host=host, call_port=call_port)

        data = data_models.MapObject.get_map_objects(map_id=map_id, password=password,
                                                     host=host, port=call_port)

        # Dijkstra apparently needs this to work
        ghost_candidates = data_models.MapObject.get_map_objects(map_id=map_id, password=password,
                                                                 host=host, port=call_port, object_type="OurRobot")
        ghost = ghost_candidates[0]
        ghost.object_type = "Can"
        ghost.direction = None

        data.append(ghost)

        response.data = json.dumps(data, cls=data_models.DataModelJsonEncoder)
        response.content_type = "json"

        # update_current_camera_view()

        return response
    except Exception as ex:
        exception_message = get_exception_message(ex)

        error_log = data_models.Log(origin=os.path.basename(__file__), message=exception_message, log_type="Error")
        error_log.create(password=password, host=host, port=call_port)

        response.data = "An error occurred - see logs"
        return response


# TODO: Implement this
def check_if_obstacles_in_the_way(map_id,  password, host, call_port):
    robot = None
    robot_candidates = data_models.MapObject.get_map_objects(map_id=map_id, object_type="OurRobot", password=password,
                                                             host=host, port=call_port)

    # Treat it as if it's good to go and when we get our response from movement the robot
    # record will be created
    if len(robot_candidates) == 0:
        return False
    else:
        robot = robot_candidates[0]

    obstacles = data_models.MapObject.get_map_objects(map_id=map_id, object_type="Can", password=password,
                                                      host=host, port=call_port)

    robot_x = robot.location[0]
    robot_y = robot.location[1]
    direction = robot.direction

    for obstacle in obstacles:
        obst_x = obstacle.location[0]
        obst_y = obstacle.location[1]

        match direction:
            case "N":
                if obst_y - 1 == robot_y:
                    return True
            case "S":
                if obst_y + 1 == robot_y:
                    return True
            case "E":
                if obst_x - 1 == robot_x:
                    return True
            case "W":
                if obst_x + 1 == robot_x:
                    return True

    return False


# Test moving the robot over the Interwebs.
# No URL params
@app.route('/testrobotconnect', methods=['GET'])
def test_robot_connect():
    response = Flask.response_class()
    response.headers.add('Access-Control-Allow-Origin', '*')

    try:
        karr_ip = __get_robot_ip()
        api_url = karr_ip + "/coffee"
        requests.get(api_url)

        response.data = "Test connect to robot successful!"
    except Exception:
        response.data = "Could not reach robot."

    return response


def process_autonomous_request(map_id, password, dijkstra_coordinates,
                               host="localhost", call_port=5432, database="RobotRadarAlpha"):
    # dijkstra_file = open('sample-data/dijkstra-test-coordinates.json')
    # dijkstra_coordinates = json.load(dijkstra_file)

    coordinates = dijkstra_coordinates.get("Coordinates")

    robot_record_candidates = data_models.MapObject.get_map_objects(password=password, map_id=map_id,
                                                                    object_type="OurRobot",
                                                                    host=host, port=call_port, database=database)

    robot_record = None

    if len(robot_record_candidates) > 0:
        robot_record = robot_record_candidates[0]
    else:
        []

    move_list = map_helper.convert_dijkstra_to_moves(dijkstra_coordinates=coordinates, robot_record=robot_record)

    return move_list


def process_other_robot_request(robot_response, map_id, password,
                                host="localhost", call_port=5432, database="RobotRadarAlpha"):
    direction = robot_response.get("orientation")
    location = robot_response.get("location")
    radar_val = robot_response.get("radar")

    robot_pos = map_helper.convert_robot_position(location)

    map_helper.update_other_robot(map_id=map_id, robot_position=robot_pos, direction=direction,
                                  password=password, host=host, port=call_port, database=database)


    found_obstacle = map_helper.obstacle_detection(map_id=map_id, direction=direction,
                                                   robot_position=robot_pos, radar_reading=radar_val,
                                                   password=password, host=host, port=call_port, database=database)

    return found_obstacle


# Only for testing purposes; test locally, do not deploy
'''
@app.route('/robotresponse', methods=['GET'])
def test_robot_response():
    robot_response_file = open('sample-data/robot-move-response.json')
    robot_response = json.load(robot_response_file)

    connection_info = database_handler.get_connection_info(request)

    password = connection_info[0]
    host = connection_info[1]
    call_port = connection_info[2]

    map_id = __get_current_map_id()

    process_robot_response(robot_response=robot_response, map_id=map_id, password=password,
                           host=host, call_port=call_port)

    data = data_models.MapObject.get_map_objects(map_id=map_id, password=password,
                                                 host=host, port=call_port)

    response = Flask.response_class()
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.data = json.dumps(data, cls=data_models.DataModelJsonEncoder)

    response.content_type = "json"

    return response
'''


def process_robot_response(robot_response, map_id, password,
                           host="localhost", call_port=5432, database="RobotRadarAlpha"):
    # robot_response_file = open('sample-data/robot-move-response.json')
    # robot_response = json.load(robot_response_file)

    direction = robot_response.get("orientation")
    location = robot_response.get("location")
    radar_val = robot_response.get("radar")

    robot_pos = map_helper.convert_robot_position(location)

    session["current_direction"] = direction
    session["current_robot_position"] = robot_pos

    map_helper.update_robot(map_id=map_id, robot_position=robot_pos, direction=direction,
                            password=password, host=host, port=call_port, database=database)

    found_obstacle = map_helper.obstacle_detection(map_id=map_id, direction=direction,
                                                   robot_position=robot_pos, radar_reading=radar_val,
                                                   password=password, host=host, port=call_port, database=database)

    return found_obstacle


# @app.route('/get_picture', methods=['GET'])
def update_current_camera_view():
    karr_ip = __get_robot_ip()
    api_url = karr_ip + "/liveStream"

    api_response = requests.post(api_url, stream=True)

    dest_dir = "panoramic-images/camera-data"

    with open(dest_dir + '/liveStream.png', 'wb') as out_file:
        shutil.copyfileobj(api_response.raw, out_file)

    return "Image retrieved"


def get_exception_message(ex):
    if hasattr(ex, 'message'):
        return str(ex.message)
    else:
        return str(ex)


# driver function
if __name__ == '__main__':
    # This is important for Docker
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
