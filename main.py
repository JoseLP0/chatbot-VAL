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
    global messages
    # Add the system message for the chatbot's identity

    # Add the user's input as part of the conversation
    messages.append({"role": "user", "content": prompt})

    # Make the API call to OpenAI to get the chatbot's response
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=messages
    )

    response = completion.choices[0].message.content

    # Display the chatbot's response to the user
    print('')
    print(f'VAL: {response}')
    print('')

    # Add the chatbot's response to the conversation history
    messages.append({"role": "system", "content": response})


# Function that runs on startup, handles the login/registration process
def startup():
    global logged_in_user, messages
    print(pyfiglet.figlet_format("ChatBot\n V A L", font="slant"))
    print("VAL: Hey I'm VAL,\nGo ahead and log in by typing '/login'. Don't have an account?\n"
          "No Problem type '/register' and I'll help you get started.\n")

    while not logged_in_user:
        response = input('Me: ').strip()
        print()

        # Handle the commands with the centralized function
        success, logged_in_user = handle_command(response, messages, logged_in_user)

        if success and logged_in_user:
            # After login, load the conversation history from MongoDB
            messages = logged_in_user.get('conversation_history', [])  # Load the previous conversation if it exists

            if not messages:  # If there are no messages yet, it's a new session
                messages.append({"role": "system", "content": 'Your name is VAL. You are a helpful assistant'})

            load_history(messages)

            return True  # Break the loop once login or registration is successful

    print(Fore.RED + "VAL: Try typing '/login' or '/register' to get started.\n"
                         "Don't feel like conversing? Type '/exit'\n")


def load_history(conversation):
    system_prompt_skipped = False  # Track if the first system message has been skipped

    for message in conversation:
        if message['role'] == 'system':
            if not system_prompt_skipped:
                system_prompt_skipped = True  # Skip the first system message
                continue
            print(f"VAL: {message['content']}\n")

        if message['role'] == 'user':
            print(f"Me: {Fore.GREEN + message['content']}\n")


if __name__ == "__main__":
    while not logged_in_user:  # Keep asking for login/registration until logged in or exit
        if not startup():
            print('VAL: Goodbye!')
            exit()
        else:
            break

    # Proceed with chatbot interactions if logged in
    print('VAL: Hello, how can I assist you today!\n')

    while True:
        reply = input('Me: ').strip()

        # Handle commands in the interaction loop
        command_success, logged_in_user = handle_command(reply, messages, logged_in_user)

        # If the command is not recognized as a login/exit command, pass it to the chatbot
        if not command_success:
            chatbot(reply)
