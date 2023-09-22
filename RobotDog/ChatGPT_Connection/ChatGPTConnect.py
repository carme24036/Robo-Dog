import os
import openai
import pyreadline as readline

# Load environment variables from a .env file
from dotenv import load_dotenv
load_dotenv()

# Initialize OpenAI client
api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = api_key

# # Import the Go1 library
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
Hello ChatGPT. You are going to be helping me control the Unitree Go1 Robot Dog. 
Here are some method definitions to control the Go1:
                    
goForward(speed: float, length_of_time: int)
goBackward(speed: float, length_of_time: int)
goLeft(speed: float, length_of_time: int)
goRight(speed: float, length_of_time: int)
turnLeft(speed: float, length_of_time: int)
turnRight(speed: float, length_of_time: int)
  
All methods accept two arguments. The first is speed with a value from 0 to 1, where 1 is full speed. The second argument is a duration in milliseconds.

Keep in mind that before we can move Go1, we need to make sure to set its mode to Go1Mode.walk.

There is a wait method in cases where we want to pause between commands. It accepts a number in milliseconds:

wait(length_of_time: int)

Please make sure that all wait commands are awaited.

For the dog to lay down, we use the following command:

setMode(Go1Mode.standDown)

and to stand up, we use

setMode(Go1Mode.standUp)

You can also change the LEDs of the robot dog using the following commands:

setLedColor(red: int, green: int, blue: int)

Where red, green, and blue are integers between 0 and 255.

Blinking the LED must always have a 2-second delay between colors.
"""

messages = [{"role": "system", "content": chat_prompt}]
user_input = input("Welcome to ChatGPT. Feel free to ask it questions.\n> ")

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

            print("\n", bot_message['content'], "\n")

            user_input = input("\n>")
        else:
            user_input = input("\nNo response, try asking again.\n>")

    except Exception as error:
        print(error)
        user_input = input("\nSomething went wrong, try asking again.\n")

# Close the readline interface
readline.write_history_file('chat_history.txt')