from json import JSONEncoder
from datetime import date, datetime
import database_handler


class Map:
    def __init__(self, id=None, created_at=None):
        self.id = id
        self.created_at = created_at

    @staticmethod
    def create(password, host="localhost", port=5432, database="RobotRadarAlpha"):
        conn = database_handler.get_connection(password=password, host=host, port=port, database=database)
        cur = conn.cursor()

        cur.execute('INSERT INTO "Map" DEFAULT VALUES returning "Id", "CreatedAt"')

        conn.commit()

        rows = cur.fetchall()

        fresh_map = Map(rows[0][0], rows[0][1])

        cur.close()
        conn.close()

        return fresh_map


class Log:
    def __init__(self, origin, message, log_type, stack_trace="", created_at=None, id=None):
        self.created_at = created_at
        self.origin = origin
        self.message = message
        self.log_type = log_type
        self.stack_trace = stack_trace
        self.id = id

    def create(self, password, host="localhost", port=5432, database="RobotRadarAlpha"):
        conn = database_handler.get_connection(password, host, database, port)
        cur = conn.cursor()

        cur.execute('INSERT INTO "Logs" ("Origin", "Message", "Type", "StackTrace")'
                    'VALUES (%s, %s, %s, %s)',
                    (self.origin,
                     self.message,
                     self.log_type,
                     self.stack_trace))

        conn.commit()

        cur.close()
        conn.close()

        print("Successfully inserted a log!")

    @staticmethod
    def get_logs(password, host="localhost", port=5432, database="RobotRadarAlpha"):
        conn = database_handler.get_connection(password=password, host=host, database=database, port=port)
        cur = conn.cursor()

        cur.execute('SELECT * FROM "Logs"')
        rows = cur.fetchall()

        logs = list()

        for row in rows:
            id = row[0]
            created_at = row[1]
            origin = row[2]
            message = row[3]
            log_type = row[4]
            stacktrace = row[5]

            log_record = Log(origin, message, log_type, stacktrace, created_at, id)
            logs.append(log_record)

        return logs

    @staticmethod
    def get_latest_logs(password, host="localhost", port=5432, database="RobotRadarAlpha"):
        conn = database_handler.get_connection(password=password, host=host, database=database, port=port)
        cur = conn.cursor()

        cur.execute('SELECT * FROM "Logs" ORDER BY "CreatedAt" DESC LIMIT 10')
        rows = cur.fetchall()

        logs = list()

        for row in rows:
            id = row[0]
            created_at = row[1]
            origin = row[2]
            message = row[3]
            log_type = row[4]
            stacktrace = row[5]

            log_record = Log(origin, message, log_type, stacktrace, created_at, id)
            logs.append(log_record)

        return logs


class MapObject:
    def __init__(self, map_id, object_type, location_x, location_y, direction=None, created_at=None, obj_id=None):
        self.map_id = map_id
        self.object_type = object_type
        self.location = (location_x, location_y)
        self.created_at = created_at
        self.direction = direction
        self.obj_id = obj_id

    def create(self, password, host="localhost", port=5432, database="RobotRadarAlpha"):
        conn = database_handler.get_connection(password, host, database, port)
        cur = conn.cursor()

        cur.execute('INSERT INTO "MapObject" ("MapId", "ObjectType", "Direction", "LocationX", "LocationY")'
                    'VALUES (%s, %s, %s, %s, %s)',
                    (self.map_id,
                     self.object_type,
                     self.direction,
                     self.location[0],
                     self.location[1]))

        conn.commit()

        cur.close()
        conn.close()

        print("Successfully inserted a map object!")

    # Update a given map object's location
    def update_map_object_location(self, password, host="localhost", port=5432, database="RobotRadarAlpha"):
        conn = database_handler.get_connection(password, host, database, port)
        cur = conn.cursor()

        if self.direction is not None:
            cur.execute('UPDATE "MapObject" SET "LocationX" = %s, "LocationY" = %s, "Direction" = %s WHERE "Id" = %s',
                        (self.location[0], self.location[1], self.direction, self.obj_id))
        else:
            cur.execute('UPDATE "MapObject" SET "LocationX" = %s, "LocationY" = %s WHERE "Id" = %s',
                        (self.location[0], self.location[1], self.obj_id))

        conn.commit()

        cur.close()
        conn.close()

        print("Successfully updated MapObject with Id %s", self.obj_id)

    @staticmethod
    def delete_obstacles(password, map_id, host="localhost", port=5432,
                         database="RobotRadarAlpha"):
        conn = database_handler.get_connection(password, host, database, port)
        cur = conn.cursor()

        cur.execute('DELETE FROM "MapObject" WHERE "MapId" = %s AND "ObjectType" = %s', (map_id, "Can"))

        conn.commit()
        cur.close()
        conn.close()
        print("Deleted all obstacles with MapId ", str(map_id))

    @staticmethod
    def get_map_objects(password, map_id=None, object_type=None, host="localhost", port=5432,
                        database="RobotRadarAlpha"):
        conn = database_handler.get_connection(password, host, database, port)
        cur = conn.cursor()

        if (map_id is not None) and (object_type is None):
            cur.execute('SELECT * FROM "MapObject" WHERE "MapId" = %s', [map_id])
        elif (map_id is not None) and (object_type is not None):
            cur.execute('SELECT * FROM "MapObject" WHERE "MapId" = %s AND "ObjectType" = %s', (map_id, object_type))
        elif (map_id is None) and (object_type is not None):
            cur.execute('SELECT * FROM "MapObject" WHERE "ObjectType" = %s', object_type)
        else:
            cur.execute('SELECT * FROM "MapObject"')

        rows = cur.fetchall()

        map_objects = MapObject.process_map_object_db_rows(rows)
        return map_objects

    @staticmethod
    def process_map_object_db_rows(rows):
        map_objects = list()

        for row in rows:
            obj_id = row[0]
            created_at = row[1]
            map_id = row[2]
            object_type = row[3]
            location_x = row[4]
            location_y = row[5]
            direction = row[6]

            map_object_record = MapObject(map_id, object_type, location_x, location_y, direction, created_at,
                                          obj_id)
            map_objects.append(map_object_record)

        return map_objects


class DataModelJsonEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, (datetime, date)):
            return o.isoformat()
        return o.__dict__


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError("Type %s not serializable" % type(obj))
