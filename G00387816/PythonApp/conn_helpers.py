import pymysql #package used for mysql interactions
import pymongo #package used for mongodb interactions

class mysql_conn:
    """
    mysql_conn - acts as a helper class for simplifying opening, closing connections and executing queries
    """
    def __init__(self):
        self.host = "localhost"
        self.user = "root"
        self.password = ""
        self.db = "moviesDB"

    def __connect__(self):
        self.conn = pymysql.connect(host="localhost", user="root", password="", db="moviesDB", cursorclass=pymysql.cursors.DictCursor)
    
    #fetch simply executes query and returns cursor object
    def fetch(self, query, param=None):
        self.__connect__()
        with self.conn:
            try:
                cursor = self.conn.cursor() #create cursor object
                if param is None:
                    cursor.execute(query) #execute query from string variable in queries.py
                else:
                    cursor.execute(query,param) #else param passed along with query, so execute query with any %s replaced with param
                return cursor
            except pymysql.err.InternalError as e:
                print("Hit InternalError - ",str(e))
            except pymysql.err.ProgrammingError as e:
                print("Check your query there was a syntax error - ", str(e))
            except Exception as e:
                print("Hit an unexpected error - ",str(e))

    def insert(self, query, param):
        self.__connect__()
        with self.conn:
            try:
                cursor = self.conn.cursor() #create cursor object
                cursor.execute(query, param) #execute query from string variable in queries.py
                self.conn.commit() #commit the executed insertion query
                return cursor
            except Exception as e:
                print(str(e))

class mongo_conn:
    """
    mysql_conn - acts as a helper class for simplifying opening, closing connections and executing queries
    """
    def __init__(self):
        self.host = "localhost"
        self.port = 27017

    def __connect__(self):
        self.client = pymongo.MongoClient(host=self.host,port=self.port)

    #fetch simply executes query and returns cursor object
    def fetch(self, query, project):
        self.__connect__()
        with self.client:
            try:
                db = self.client['movieScriptsDB']
                collection = db['movieScripts']
                return collection.find(query,project) #return result of find()
                
            except pymysql.err.InternalError as e:
                print("Hit InternalError - ",str(e))
            except pymysql.err.ProgrammingError as e:
                print("Check your query there was a syntax error - ", str(e))
            except Exception as e:
                print("Hit an unexpected error - ",str(e))

    def insert(self, query):
        self.__connect__()
        with self.conn:
            try:
                db = self.client['movieScriptsDB']
                collection = db['movieScripts']
                return collection.insert_one(query) #return result of find()
            #using pymongo error handling to pick up duplicate key error
            #first attempt used collection.count_documents() to determine whether document existed but collection.insert_one()returns error message on duplicate keys
            except pymongo.errors.DuplicateKeyError as e:
                print(f"\n*** ERROR *** Movie Script with id {input_film_id} already exists")
            #catch any other errors that may occur
            except Exception as e:
                print(f"Hit an error, see below for detail:\n{str(e)}")
