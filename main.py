from views import View
import sys





if __name__ == "__main__":
    print(sys.prefix)

    # db = Database("localhost", "appuser", "appuser", "cms_live")
    # db.create_connection()


    myview=View()
    myview.create_main_window()


    # create_tables()  # Create tables if they don't exist
    # display_users()   # Display existing users
    # create_user("Alice", "alice@example.com")  # Example of adding a use