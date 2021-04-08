import pymysql
import queries

#declaring global var cached_studios to later store result of user picking menu item 3 for any subsequent requests
cached_studios = None

def view_films():
    print("\nFilms") #Text to display current menu item
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

    conn = pymysql.connect(host="localhost", user="root", password="", db="moviesDB", cursorclass=pymysql.cursors.DictCursor)
    #connection object to local mysql db moviesDB

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
    conn = pymysql.connect(host="localhost", user="root", password="", db="moviesDB", cursorclass=pymysql.cursors.DictCursor)
    #connection object to local mysql db moviesDB

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
            #gender must be either 'Male' or 'Female'
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
    print("View subbed FILMS")

def add_new_movscript():
    print("Add new movie script")

def main_menu():
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

if __name__ == "__main__":
    main_menu()