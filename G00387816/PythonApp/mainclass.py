import pymysql #package used for mysql interactions
import pymongo #package used for mongodb interactions

import queries #python file holding variables for mysql queries

#declaring global var cached_studios to later store result of user picking menu item 3 for any subsequent requests
cached_studios = None



class mysql_conn:
    def __init__(self):
        self.host = "localhost"
        self.user = "root"
        self.password = ""
        self.db = "moviesDB"

    def __connect__(self):
        self.conn = pymysql.connect(host="localhost", user="root", password="", db="moviesDB", cursorclass=pymysql.cursors.DictCursor)
    
    def fetch(self, query):
        self.__connect__()
        with self.conn:
            try:
                cursor = self.conn.cursor() #create cursor object
                cursor.execute(queries.list_films_actors) #execute query from string variable in queries.py
                return cursor
            except Exception as e:
                print(str(e))


def view_films_alt():
    test_inst = mysql_conn()
    test = test_inst.fetch(queries.list_films_actors)
    t2 = test.fetchmany(5)
    for row in t2:
        print(row)
    for row in t2:
        print(row)
    t2 = test.fetchmany(5)
    for row in t2:
        print(row)

    test_inst2 = mysql_conn()
    test2 = test_inst2.fetch(queries.list_films_actors)
    test2.fetchmany(10)
    #for row in test2:
        #print(test2)


view_films_alt()

def view_films():
    '''
    view_films displays film title and actor names from the Films table in groups of 5 until user exits
    user is prompted to enter q to quit, anything else loads the next 5
    '''
    #Text to display current menu item
    print("\nFilms") 
    print("------")
    conn = pymysql.connect(host="localhost", user="root", password="", db="moviesDB", cursorclass=pymysql.cursors.DictCursor)
    #connection object to local mysql db moviesDB

    #with to automatically close connection once code finishes executing
    with conn:
        try:
            cursor = conn.cursor() #create cursor object
            cursor.execute(queries.list_films_actors) #execute query from string variable in queries.py

            show_results = True #while true want loop to continue
            #Loop until letter 'q' is entered by user
            while show_results == True:
                query_result = cursor.fetchmany(5)
                for i in range(5):
                    print(f"{query_result[i]['FilmName']:15} || {query_result[i]['ActorName']:15}")
                #if user enters 'q' or 'Q' exit
                if str(input("--------Q to quit--------")).lower() == 'q':
                    show_results=False

        except pymysql.err.InternalError as e:
            print("Hit InternalError - ",str(e))
        except pymysql.err.ProgrammingError as e:
            print("Check your query there was a syntax error - ", str(e))
        except Exception as e:
            print("Hit an unexpected error - ",str(e))

def view_actors():
    '''
    view_actors prompts user to enter year of birth and gender for actors in the moviesDB and displays their details 
    if records found that match the user request
    '''
    #connection object to local mysql db moviesDB
    conn = pymysql.connect(host="localhost", user="root", password="", db="moviesDB", cursorclass=pymysql.cursors.DictCursor)

    #with to automatically close connection once code finishes executing
    with conn:
        try:
            #print out current menu selection
            print("\nActors")
            print("------")
            #year_dob must be integer, casting as str to avoid hitting an exception if non-int entered
            year_dob = str(input("Year of Birth : "))

            #use while loop to reprompt if isnumeric() funtion returns false so will continue until what user enters is a integer-like string
            while year_dob.isnumeric() == False:
                year_dob = str(input("Year of Birth : "))

            #gender must be either 'Male' or 'Female'
            gender = str(input("Gender (Male/Female) : "))

            #use while loop to reprompt till 'Male' or 'Female' entered
            while gender not in ['Male', 'Female']:
                gender = str(input("Gender (Male/Female) : "))
            
            cursor = conn.cursor() #create cursor object
            
            cursor.execute(queries.search_actor_gender_dob,(year_dob,gender)) #supply the confirmed values for year_dob and gender

            query_result = cursor.fetchall() #get all rows from the executed cursor
            
            print("\nActors")
            print("------")
            #got the maximum length of each of the fields to be printed out for consistent format spacing using max(length()) on the table in mysql 
            for row in query_result:
                print(f"{row['ActorName']:27} | {row['DobMonth']:9} | {row['ActorGender']:6}")

        except pymysql.err.InternalError as e:
            print("Hit InternalError - ",str(e))
        except pymysql.err.ProgrammingError as e:
            print("Check your query there was a syntax error - ", str(e))
        except Exception as e:
            print("Hit an unexpected error - ",str(e))

def view_studios():
    '''
    view_studios shows all the film studios from the moviesDB database studio table in ascending studio id order
    '''
    global cached_studios #referencing the global variable cached_studios within the function
    #if cached_studios is None then query hasn't been ran before, therefore run the query and store all the fetched rows in the global var
    if cached_studios is None:
        conn = pymysql.connect(host="localhost", user="root", password="", db="moviesDB", cursorclass=pymysql.cursors.DictCursor)
        #connection object to local mysql db moviesDB

        #with to automatically close connection once code finishes executing
        with conn:
            try:
                #print out current menu selection
                print("\nStudios")
                print("------")
                
                cursor = conn.cursor() #create cursor object
                
                cursor.execute(queries.list_studios)

                cached_studios = cursor.fetchall() #get all rows from the executed cursor
                
                #got the maximum length of each of the fields to be printed out for consistent format spacing using max(length()) on the table in mysql 
                for row in cached_studios:
                    print(f"{row['StudioID']:2} | {row['StudioName']:28}")

            except pymysql.err.InternalError as e:
                print("Hit InternalError - ",str(e))
            except pymysql.err.ProgrammingError as e:
                print("Check your query there was a syntax error - ", str(e))
            except Exception as e:
                print("Hit an unexpected error - ",str(e))
    #Else the query must have been ran earlier
    else:
        for row in cached_studios:
            print(f"{row['StudioID']:2} | {row['StudioName']:28}")


def add_new_country():
    '''
    add_new_country allows a user to make a new entry to the country table of the moviesDB Database
    if country or id already exists the user is informed via an error message
    '''
    #connection object to local mysql db moviesDB
    conn = pymysql.connect(host="localhost", user="root", password="", db="moviesDB", cursorclass=pymysql.cursors.DictCursor)

    #with to automatically close connection once code finishes executing
    with conn:
        try:
            #print out current menu selection
            print("\nAdd New Country")
            print("---------------")
            
            #year_dob must be integer, casting as str to avoid hitting an exception if non-int entered
            country_id = str(input("Country ID : "))

            #use while loop to reprompt if isnumeric() funtion returns false so will continue until what user enters is a integer-like string
            while country_id.isnumeric() == False:
                year_dob = str(input("Country ID : "))

            #gender should be either 'Male' or 'Female'
            country_name = str(input("Country Name : "))

            #use while loop to reprompt till a non blank value entered
            while country_name in ['']:
                country_name = str(input("Country Name : "))

            cursor = conn.cursor() #create cursor object
            
            insert_row = cursor.execute(queries.insert_country, (country_id, country_name))
            conn.commit() #commit the executed insertion query
            #If we reach this point without hitting an except then insertion was succesfull
            #just to make fully sure though check insert_row is 1, as cursor.execute returns an int representing how many rows were affected
            if insert_row == 1:
                print(f"Country {country_id}, {country_name} added to the Database!")

        except pymysql.err.IntegrityError as e:
            print(f"*** ERROR *** you have entered a duplicate Country ID {country_id} or Country Name {country_name} for more detailed error message see next line:\n {str(e)}")
        except pymysql.err.InternalError as e:
            print("Hit InternalError - ",str(e))
        except pymysql.err.ProgrammingError as e:
            print("Check your query there was a syntax error - ", str(e))
        except Exception as e:
            print("Hit an unexpected error - ",str(e))


def view_subtitled():
    '''
    view_subtitled prompts user to enter a subtitle language
    it then finds each film in the mongodb movieScripts Collection that has that language,
    using the id for that document it then returns films from the mysql moviesdb film table that have a matching id
    the film name and a abbreviated synopsis is then displayed.
    '''
    print("\nMovies with Subtitles")
    print("---------------------")
    #input_language will store user submitted subtitle language
    input_language = ''
    #while input_language is a blank str continue to request input from user e.g. if they enter blank
    while input_language == '':
        input_language = str(input("Enter Subtitle Language : "))
    
    #set query for mongo find using user input as what documents to find
    mongo_sub_query = {"subtitles": input_language}
    #set project for mongo find to only include id and subtitles (subtitles not necessary but convenient to have for testing)
    mongo_sub_project = {"_id":1, "subtitles":1}

    #set up client to local instance of MongoDB
    client = pymongo.MongoClient(host='localhost',port=27017)
    with client:
        #try to query the mongoDB
        try:
            db = client['movieScriptsDB']
            collection = db['movieScripts']
            subtitled_film_result = collection.find(mongo_sub_query,mongo_sub_project) #query mongo and store result
        except Exception as e:
            print(f"Hit an error, see below for detail:\n{str(e)}")
            #return

    list_subtitled_film_result = list(subtitled_film_result) #convert result from mongoDB to list for parsing
    #check length of the list is greater than 0, if it is greater than 0 films have been found with subtitle user entered
    if len(list_subtitled_film_result) > 0:

        #for every remaining item in result list, step through and add it to the query_input_str, with comma seperating from last value of the var
        list_input = []
        for item in list_subtitled_film_result:
            list_input.append(item["_id"])
    
        #connection object to local mysql db moviesDB
        conn = pymysql.connect(host="localhost", user="root", password="", db="moviesDB", cursorclass=pymysql.cursors.DictCursor)

        #using with to automatically close connection once code finishes executing
        with conn:
            try:
                cursor = conn.cursor() #create cursor object
                
                #format_s_placeholder will later be used insert the correct number of %s to queries.list_fimls_by_id
                format_s_placeholder = ','.join(['%s'] * len(list_input))
                #in this execute, passing in a list of varying length so the number of %s needs to change to reflect that
                cursor.execute(queries.list_films_by_id.format(s_placeholder=format_s_placeholder),list_input) #supply the confirmed values for year_dob and gender

                query_result = cursor.fetchall() #get all rows from the executed cursor
                print(f"\nMovies with {input_language} subtitles")
                print("---------------------------------------")
                #got the maximum length of each of the fields to be printed out for consistent format spacing using max(length()) on the table in mysql 
                for row in query_result:
                    print(f"{row['FilmName']:19} | {row['FilmSynopsis'][:30]}")

            except pymysql.err.InternalError as e:
                print("Hit InternalError - ",str(e))
            except pymysql.err.ProgrammingError as e:
                print("Check your query there was a syntax error - ", str(e))
            except Exception as e:
                print("Hit an unexpected error - ",str(e))

    #else no film was found with user entered subtitle language so print to inform them
    else: 
        print(f"\nUnfortunately the subtitle language {input_language} returned no results.")

def add_new_movscript():
    '''
    add_new_movscript allows user to add a new script to the mongodb movieScripts collection and can add as many keywords and subtitles as they would like
    if a document of the same _id already exists or if a film doesn't exist by that id, then the user is informed with an error message 
    '''
    #print the current menu item
    print("\n Add New Movie Script")
    print("---------------------")
    #input_film_id will store the id for a new film script to be added to database
    input_film_id = ''
    #while input_film_id is a blank str continue to request input from user e.g. if they enter blank
    while input_film_id == '':
        try:
            input_film_id = int(input("ID : ")) #must enter a int number here
        except Exception as e:
            print(f"Entered something wrong here, probably not a number, see error below for detail - \n{str(e)}")

    #Take user input for keywords, store in list, stop adding to list when -1 entered
    keyword_list = []
    input_keyword = str(input("Keyword (-1 to end) : "))
    while input_keyword != "-1":
        keyword_list.append(input_keyword)
        input_keyword = str(input("Keyword (-1 to end) : "))

    #Take user input for subtitles, store in list, stop adding to list when -1 entered
    subtitle_list = []
    input_subtitle = str(input("Subtitles Language (-1 to end) : "))
    while input_subtitle != "-1":
        subtitle_list.append(input_subtitle)
        input_subtitle = str(input("Subtitles Language (-1 to end) : "))

    #additional check for whether film ID exists in moviesDB Film Table, if it doesn't return an error
    #connection object to local mysql db moviesDB
    conn = pymysql.connect(host="localhost", user="root", password="", db="moviesDB", cursorclass=pymysql.cursors.DictCursor)

    #using with to automatically close connection once code finishes executing
    with conn:
        try:
            cursor = conn.cursor() #create cursor object
            
            #in this execute, passing in a list of varying length so the number of %s needs to change to reflect that
            cursor.execute(queries.count_films_by_id, (input_film_id)) #supply the confirmed values for year_dob and gender

            query_result = cursor.fetchall() #get all rows from the executed cursor
            #got the maximum length of each of the fields to be printed out for consistent format spacing using max(length()) on the table in mysql 
            if(query_result[0]['count'] == 0):
                return(print(f"*** ERROR *** Film with id {input_film_id} does not exist in moviesDB"))

        except pymysql.err.InternalError as e:
            print("Hit InternalError - ",str(e))
        except pymysql.err.ProgrammingError as e:
            print("Check your query there was a syntax error - ", str(e))
        except Exception as e:
            print("Hit an unexpected error - ",str(e))

    #having gotten this far, no duplicate id has been seen in mongodb collection and film exists in moviesDB, so it is safe to add new film subtitles document to mongodb collection
    mongo_subtitle_insert = {"_id":input_film_id, "keywords": keyword_list, "subtitles": subtitle_list}
    client = pymongo.MongoClient(host='localhost',port=27017)
    with client:
        #try to query the mongoDB
        try:
            #specify the db and collection
            db = client['movieScriptsDB']
            collection = db['movieScripts']

            subtitled_film_result = collection.insert_one(mongo_subtitle_insert)
            
            print(f"MovieScript: {input_film_id} added to the database")

        #using pymongo error handling to pick up duplicate key error
        #first attempt used collection.count_documents() to determine whether document existed but collection.insert_one()returns error message on duplicate keys
        except pymongo.errors.DuplicateKeyError as e:
            print(f"\n*** ERROR *** Movie Script with id {input_film_id} already exists")
        #catch any other errors that may occur
        except Exception as e:
            print(f"Hit an error, see below for detail:\n{str(e)}")

def main_menu():
    '''
    main_menu is first function called on running this file
    calls other functions based on users input, exits on user entering x
    '''
    selection = None
    while selection != "x":
        print("\nMovies DB")
        print("---------")
        print("\nMENU")
        print("====")
        print("1 - View Films")
        print("2 - View Actors by Year of Birth & Gender")
        print("3 - View Studios")
        print("4 - Add New Country")
        print("5 - View Movie with Subtitles")
        print("6 - Add New MovieScript")
        print("x - Exit Application")
        selection = str(input("Choice: "))
        if selection =="1":
            view_films()
        elif selection == "2":
            view_actors()
        elif selection =="3":
            view_studios()
        elif selection =="4":
            add_new_country()
        elif selection == "5":
            view_subtitled()
        elif selection =="6":
            add_new_movscript()