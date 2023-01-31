# Followed code example from here:
# https://www.digitalocean.com/community/tutorials/how-to-use-a-postgresql-database-in-a-flask-application

import psycopg2
import ast


def get_connection(password, host, database, port=5432):
    return psycopg2.connect(
        host=host,
        database=database,
        user="flaskuser",
        password=password,
        port=port)


# For the love of all that is good, just and kind in the world
# DO NOT TOUCH THIS UNLESS YOU ABSOLUTELY HAVE TO!!!
def get_connection_info(request):
    is_test = request.args.get('istest')
    is_remote = request.args.get('remote')
    password = request.args.get("password")

    call_port = 5432
    host = 'localhost'

    if (is_test is None or ast.literal_eval(is_test.capitalize())) \
            and (is_remote is None or not ast.literal_eval(is_remote.capitalize())):
        pass
    elif is_remote:
        host = "<REMOTE IP>"
        call_port = 36000
    else:
        host = "localhost"
        call_port = 36000

    return password, host, call_port
