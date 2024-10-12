from colorama import Fore
from user_management import login, register_users

logged_in_user = None


def handle_command(command):
    global logged_in_user

    # First check if is an exit command
    if isinstance(command, str) and command.lower() in ["/exit", "/quit", "/close", "/stop", "/end", "logout"]:
        print(Fore.RED + 'VAL: Exiting... Goodbye!')
        exit()

    # Handle login command
    elif command == '/login':
        logged_in_user = login()  # Update the logged-in user if successful
        if logged_in_user:
            print(Fore.CYAN + 'VAL: You are now logged in as', logged_in_user['username'])
        return True  # Login successful

    # Handle registration command
    elif command == '/register':
        email, username, password = register_users()
        print(Fore.CYAN + 'VAL: Registration complete!\n')

        # Automatically log in after registration
        logged_in_user = login(email=email, password=password)
        if logged_in_user:
            print(Fore.CYAN + 'VAL: You are now logged in as', logged_in_user['username'])
            return True  # Registration and login successful

        return False

    else:
        return False  # Return False for unrecognized commands
