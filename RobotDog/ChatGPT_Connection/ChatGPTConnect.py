import os
import openai

# Load environment variables from a .env file
from dotenv import load_dotenv
load_dotenv()

# Initialize OpenAI client
api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = api_key

# Function to extract code blocks from content
import re
def extract_code(content):
    regex = r"```([^\n]*)\n([\s\S]*?)```"
    matches = re.finditer(regex, content)
    code_blocks = [{"language": match.group(1).strip(), "code_block": match.group(2).strip()} for match in matches]
    return code_blocks

chat_prompt = """
Hello ChatGPT. You are going to be helping me control the Unitree Go1 Robot dog. 

We use the code in the github repo at https://github.com/unitreerobotics/unitree_legged_sdk in the example_py folder to make the dog do things, such as walk, run, and change LED colors. 
The IP Address of the dog is 172.16.3.197.
"""

messages = [{"role": "system", "content": chat_prompt}]
user_input = input("Welcome to ChatGPT. Feel free to ask questions. To exit the program, type 'quit'.\n> ")

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

            print("\nBot-", bot_message['content'])

            user_input = input("\n>")
        else:
            user_input = input("\nNo response, try asking again.\n>")

    except Exception as error:
        print(error)
        user_input = input("\nSomething went wrong, try asking again.\n")

