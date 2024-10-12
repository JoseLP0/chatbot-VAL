from pymongo import MongoClient
import os
import certifi
from dotenv import load_dotenv
import re
import bcrypt
from colorama import Fore, init


load_dotenv()
init(autoreset=True)

# Connect to MongoDB
connection_string = os.getenv('MONGO_URL')
client = MongoClient(connection_string, tlsCAFile=certifi.where())

chatbot_db = client['chatbot_db']
users_col = chatbot_db.users
history_col = chatbot_db.history

users_col.create_index("email", unique=True)
users_col.create_index("username", unique=True)


def register_users():
    print(Fore.CYAN + 'VAL: Enter a email and password.\n')
    # Loop until a valid email is provided
    while True:
        email = check_exit(input('Enter Email: ').lower())
        if not is_email_valid(email):
            print(Fore.RED + 'VAL: Invalid email format. Please try again.')
        elif users_col.find_one({"email": email}):
            print(Fore.RED + 'VAL: This email is already registered. Please use a different one.')
        else:
            break  # Exit the loop when email is valid and not registered

    # Loop until a valid username is provided
    while True:
        username = check_exit(input('Enter Username: ').lower())
        if users_col.find_one({'username': username}):
            print(Fore.RED + 'VAL: This username is already taken. Please choose a different one.')
        else:
            break  # Exit the loop when username is valid and not taken

    # Loop until a valid password is provided
    while True:
        password = check_exit(input('Enter Password: '))
        if not is_password_valid(password):
            print(Fore.RED + 'VAL: Password must be at least 8 characters long, contain an uppercase letter, '
                             'a lowercase letter,'
                             'a number, and a special character.')
        else:
            break  # Exit the loop when password is valid

    # Hash the password before storing
    hashed_password = hash_password(password)

    # Insert the new user into the collection
    reg_doc = {
        'email': email,
        'username': username,
        'password': hashed_password
    }

    users_col.insert_one(reg_doc)
    # print(f'Document inserted with id: {result.inserted_id}')

    return email, username, password


def login(email=None, password=None):
    print(Fore.CYAN + 'VAL: Enter a email and password.\n')
    while True:
        # If email and password are not provided (manual login), ask for them
        if not email or not password:
            email = check_exit(input('Enter Email: ').lower())
            password = check_exit(input('Enter Password: '))
        # Find the user in the database
        user = users_col.find_one({'email': email})

        if user:
            # Check if the provided password matches the stored hashed password
            if check_password(user['password'], password):
                print(Fore.CYAN + 'VAL: Login successful!\n')
                print(user)
                return user  # Set the logged_in_user to the user data
            else:
                print(Fore.RED + '\nVAL: Incorrect password. Please try again.\n')
                email = None
                password = None
        else:
            print(Fore.RED + '\nVAL: No account found with this email. Please try again.\n')
            email = None
            password = None


def is_email_valid(email):
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return bool(re.match(email_regex, email))


# Validate password complexity
def is_password_valid(password):
    if len(password) < 8:
        return False
    if not re.search(r'[A-Z]', password):
        return False
    if not re.search(r'[a-z]', password):
        return False
    if not re.search(r'[0-9]', password):
        return False
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False
    return True


def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password


# Verify password when logging in
def check_password(stored_password, provided_password):
    return bcrypt.checkpw(provided_password.encode('utf-8'), stored_password)


# Checks for exit commands in login and registration
def check_exit(input_str):
    if input_str.lower() in ["/exit", "/quit", "/close", "/stop", "/end", "logout"]:
        print(Fore.RED + '\nVAL: Exiting... Goodbye!')
        exit()  # Exit the program
    return input_str
