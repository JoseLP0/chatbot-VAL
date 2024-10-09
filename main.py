import os
from dotenv import load_dotenv
from openai import OpenAI
import pyfiglet

load_dotenv()
client = OpenAI(api_key=os.getenv('API_KEY'))
messages = []


def chatbot(prompt):
    messages.append({"role": "system", "content": "Your name is VAL. You are a helpful assistant."})
    messages.append({"role": "user", "content": prompt})

    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=messages
    )

    print("")
    print(f"VAL: {completion.choices[0].message.content}")
    print("")

    messages.append({"role": "system", "content": completion.choices[0].message.content})


if __name__ == "__main__":
    print(pyfiglet.figlet_format("ChatBot\n V A L", font="slant"))
    print('VAL: How can I help?')
    print('')

    while True:
        reply = input("Me: ")

        if reply in ["exit", "quit", "close", "stop", "end"]:
            break

        chatbot(reply)

    print()
    print("VAL: Bye!")
