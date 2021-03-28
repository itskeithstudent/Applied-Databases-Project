import pymysql

def view_films():
    print("View FILMS")

def view_actors():
    print("View acting")

def view_studios():
    print("View studs")

def add_new_country():
    print("add country")

def view_subtitled():
    print("View subbed FILMS")

def add_new_movscript():
    print("Add new movie script")

def main_menu():
    selection = None
    while selection != "x":
        print("Movies DB")
        print("---------")
        print("\n")
        print("MENU")
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