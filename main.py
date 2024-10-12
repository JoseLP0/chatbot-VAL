import os
from dotenv import load_dotenv
from openai import OpenAI
import pyfiglet
from colorama import Fore, init
from commands import handle_command

load_dotenv()
client = OpenAI(api_key=os.getenv('API_KEY'))
messages = []
logged_in_user = False  # Track logged-in user
init(autoreset=True)


def chatbot(prompt):
    # Add the system message for the chatbot's identity
    messages.append({"role": "system", "content": 'Your name is VAL. You are a helpful assistant'})

    # Add the user's input as part of the conversation
    messages.append({"role": "user", "content": prompt})

    # Make the API call to OpenAI to get the chatbot's response
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=messages
    )

    # Display the chatbot's response to the user
    print('')
    print(f'VAL: {completion.choices[0].message.content}')
    print('')

    # Add the chatbot's response to the conversation history
    messages.append({"role": "system", "content": completion.choices[0].message.content})


# Function that runs on startup, handles the login/registration process
def startup():
    global logged_in_user
    print(pyfiglet.figlet_format("ChatBot\n V A L", font="slant"))
    print("VAL: Hey I'm VAL,\nGo ahead and log in by typing '/login'. Don't have an account?\n"
          "No Problem type '/register' and I'll help you get started.\n")

    while not logged_in_user:
        response = input('Me: ').strip()
        print()

        # Handle the commands with the centralized function
        if handle_command(response):
            return True  # Break loop when login or registration is successful

        print(Fore.RED + "VAL: Try typing '/login' or '/register' to get started.\n"
                         "Don't feel like conversing? Type '/exit'\n")


if __name__ == "__main__":
    while not logged_in_user:  # Keep asking for login/registration until logged in or exit
        if not startup():
            print('VAL: Goodbye!')
            exit()
        else:
            break

    # Proceed with chatbot interactions if logged in
    print('\nVAL: Hello, how can I assist you today!\n')

    while True:
        reply = input('Me: ').strip()

        # Handle commands in the interaction loop
        handle_command(reply)

        # Pass other inputs to the chatbot
        chatbot(reply)
