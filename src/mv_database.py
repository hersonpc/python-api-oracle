import os
import cx_Oracle
import json
from bson import json_util
from datetime import datetime
from redis import Redis

redis = Redis(host = 'redis', port = 6379)


def connect():
    ORACLE_HOME = os.environ.get('ORACLE_HOME')
    USERNAME = os.environ.get('ORACLE_USERNAME')
    PASSWORD = os.environ.get('ORACLE_PASSWORD')
    SERVER = os.environ.get('ORACLE_SERVER')
    DATABASE = os.environ.get('ORACLE_DATABASE')
    
    # redis.set('test', 'Tested.', ex=10)
    # print("REDIS ---->", redis.get('test'))
    # print(f"- Oracle: {ORACLE_HOME}, Server: {SERVER}, Database: {DATABASE}")

    connection = cx_Oracle.connect(USERNAME, PASSWORD, f"{SERVER}/{DATABASE}", encoding="UTF-8")
    # print(f"- Oracle {SERVER}, version {connection.version}")
    return(connection)


class dotdict(dict):
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


def get_results(db_cursor):
    desc = [d[0] for d in db_cursor.description]
    results = [dotdict(dict(zip(desc, res))) for res in db_cursor.fetchall()]
    return results


def execute(connection, sql_query):
    cursor = connection.cursor()
    cursor.execute(sql_query)
    results = get_results(cursor)
    return(results, cursor)


def read_sql(file_name):
    with open(file_name, encoding="utf-8") as f:
        sql_query = f.read()
    return(sql_query)


def execute_file(connection, file_name):
    with open(file_name, encoding="utf-8") as f:
        sql_query = f.read()
    # print(sql_query)
    
    return(execute(connection, sql_query))


def sql(sql_query, verbose = False):
    connection = connect()
    started_at = datetime.now()
    if(verbose):
        print(f"- Started sql query at {started_at:%Y-%m-%d_%H:%M:%S.%f }")
    dataset, cursor = execute(connection, sql_query)
    if(verbose):
        print(f"- Elapsed time: {(datetime.now() - started_at).total_seconds()} secs")
    
    connection.close()
    return(dataset)

def cache_or_sql(key, sql_query, timeout = 60):
    if(redis.exists(key)):
        # print('<< Read from cache')
        dataset = json.loads(redis.get(key).decode('utf-8'), object_hook=json_util.object_hook)
    else:
        print(f'<< Read from DB :: {key}')
        dataset = sql(sql_query)
        redis.set(key, json.dumps(dataset, default=json_util.default), ex = timeout)
    return(dataset)



def sql_file(sql_filename, verbose = False, timeout = 30):
    connection = connect()
    started_at = datetime.now()
    if(verbose):
        print(f"- Started sql query at {started_at:%Y-%m-%d_%H:%M:%S.%f }")
    if(redis.exists(sql_filename)):
        # print('<< Read from cache')
        dataset = json.loads(redis.get(sql_filename).decode('utf-8'), object_hook=json_util.object_hook)
    else:
        print(f'<< Read from DB :: {sql_filename}')
        dataset, cursor = execute_file(connection, sql_filename)
        redis.set(sql_filename, json.dumps(dataset, default=json_util.default), ex = timeout)
    if(verbose):
        print(f"- Elapsed time: {(datetime.now() - started_at).total_seconds()} secs")
    
    connection.close()
    return(dataset)