import os
import openai

# Load environment variables from a .env file
from dotenv import load_dotenv
load_dotenv()

# Initialize OpenAI client
api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = api_key

# Import the Go1 library
# from droneblocks.go1_js import Go1, Go1Mode
# dog = Go1()
# dog.init()
# dog.set_mode(Go1Mode.stand)
# # dog.go_forward(0.25, 2000)

# Function to extract code blocks from content
import re
def extract_code(content):
    regex = r"```([^\n]*)\n([\s\S]*?)```"
    matches = re.finditer(regex, content)
    code_blocks = [{"language": match.group(1).strip(), "code_block": match.group(2).strip()} for match in matches]
    return code_blocks

chat_prompt = """
Hello ChatGPT
"""

messages = [{"role": "system", "content": chat_prompt}]
user_input = input("Welcome to ChatGPT. Feel free to ask questions.\n> ")

bot_message = ""

while user_input != "quit":
    messages.append({"role": "user", "content": user_input})

    try:
        chat_completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
        )

        bot_message = chat_completion['choices'][0]['message']

        if bot_message:
            messages.append(bot_message)

            code_block = extract_code(bot_message['content'])

            print("\n Bot-", bot_message['content'], "\n")

            user_input = input("\n>")
        else:
            user_input = input("\nNo response, try asking again.\n>")

    except Exception as error:
        print(error)
        user_input = input("\nSomething went wrong, try asking again.\n")

