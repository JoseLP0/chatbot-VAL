from colorama import Fore
from user_management import login, register_users, save_conversation_history


def handle_command(command, messages, logged_in_user):
    # First check if is an exit command
    if isinstance(command, str) and command.lower() in ["/exit", "/quit", "/close", "/stop", "/end", "logout"]:
        save_conversation_history(logged_in_user['email'], messages)  # Save conversation history
        print(Fore.RED + 'VAL: Exiting... Goodbye!')
        exit()

    # Handle login command
    elif command == '/login':
        print(Fore.CYAN + 'VAL: Enter a email and password.\n')
        while True:
            email = input('Enter Email: ').lower()
            password = input('Enter Password: ')
            logged_in_user = login(email=email, password=password)  # Update the logged-in user if successful
            if logged_in_user:
                print(Fore.CYAN + 'VAL: You are now logged in as', logged_in_user['username'], '\n')
                return True, logged_in_user  # Login successful

    # Handle registration command
    elif command == '/register':
        email, username, password = register_users()
        print(Fore.CYAN + 'VAL: Registration complete!\n')

        # Automatically log in after registration
        logged_in_user = login(email=email, password=password)
        if logged_in_user:
            print(Fore.CYAN + 'VAL: You are now logged in as', logged_in_user['username'])
            return True, logged_in_user  # Registration and login successful

        return False, logged_in_user

    else:
        return False, logged_in_user  # Return False for unrecognized commands
