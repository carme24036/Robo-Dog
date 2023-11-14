# This program was written and edited by Carmen Cedano. Development began in September 2023.  
# This is the Python version of the ChatGPT-RoboDog project. The JavaScript version is slightly different.  
# It uses most of the same functions and works the same way as the JavaScript version but with a few changes. 

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------- #

# Import modules
import os                                           # Provides a way to interact with and manipulate aspects of the operating system that is running the code
import openai                                       # OpenAI module needed to communicate with ChatGPT API
from dotenv import load_dotenv                      # Lets the program load/read .env files
import re                                           # Support for regular expressions

# Load environment variables from a .env file
load_dotenv()
 
# Initialize OpenAI module
api_key = os.getenv("OPENAI_API_KEY")       # Gets openai API key from the .env file for use in this program
openai.api_key = api_key

def extract_code(content):
    '''
    The following function will only be used when ChatGPT sends a response that involves code.
    It will extract code blocks from ChatGPT's response using a regular expression.
    '''
    regex = r"```([^\n]*)\n([\s\S]*?)```"
    matches = re.finditer(regex, content)
    code_blocks = [{"language": "python", "code_block": match.group(2).strip()} for match in matches]
    return code_blocks

# This is the initial message that is sent to ChatGPT when the program is run. It tells ChatGPT how to control the robot dog so that it can make programs from it.
# It contains some code from the example_walk.py file to give ChatGPT an example of some commands that can make the dog walk. 
chat_prompt = """
Hello ChatGPT. You are going to be helping me control the Unitree Go1 Robot dog. 

We use the following code to be able to tell the Robot Dog to do commands, such as walk and crouch:

First, we import these modules:
sys
time
math
numpy

After those are imported, make sure to add the following code:

sys.path.append('/lib/python/arm64')
import robot_interface as sdk

That code adds a path to the Python library and imports the module from the library that was added to the path.

The following code is what will make the dog walk:

if __name__ == '__main__':

    HIGHLEVEL = 0xee
    LOWLEVEL  = 0xff
    
    udp=sdk.UPD(HIGHLEVEL, 8080, ipAddress, 8082)
    # ipAddress = 172.16.3.197

    cmd = sdk.HighCmd()
    state = sdk.HighState()
    udp.InitCmdData(cmd)

    motiontime = 0
    while True:
        time.sleep(0.002)
        motiontime = motiontime + 1

        udp.Recv()
        udp.GetRecv(state)

        cmd.mode = 0               # 0:idle, default stand      1:forced stand     2:walk continuously
        cmd.gaitType = 0           # Refers to the specific sequence of leg movements used in locomotion (the ability to move from one place to another).
        cmd.speedLevel = 0         # This controls the level of speed
        cmd.footRaiseHeight = 0    # This is how high the foot of the dog is raised
        cmd.bodyHeight = 0         # This changes the height of the dog's body
        cmd.euler = [0, 0, 0]      # Specifies the orientation of the robot dog's body in terms of Euler angles.
        cmd.velocity = [0, 0]      # This is what controls the velocity/speed
        cmd.yawSpeed = 0.0         # Controls the yaw rotation speed of the robot dog. Yaw rotation refers to the rotation around the vertical axis (typically the Z-axis) of the robot's body.
        cmd.reserve = 0            # Reserved variable 

        # Here is an example of a movement the Robot Dog can do: 
        if(motiontime > 0 and motiontime < 1000):
            cmd.mode = 1
            cmd.euler = [-0.3, 0, 0]

        # Here is another example of a movement:
        if(motiontime > 6000 and motiontime < 7000):
            cmd.mode = 1
            cmd.bodyHeight = -0.2
    
These last two commands end the program:

udp.SetSend(cmd)
udp.Send()

If the user asks you for code, please make it one single continuous program so that it's easy to copy, paste and run. 
"""

# This variable is what keeps track of what messages were sent to ChatGPT from the user and recieved from ChatGPT to the user
messages = [{"role": "system", "content": chat_prompt}]
user_input = input("Welcome to ChatGPT. Feel free to ask questions. To exit the program, type 'quit'.\n\n> ")

bot_message = "" # ChatGPT's response/message
code_block = ""

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
            if bot_message: 
                user_input = input("Would you like to see the raw unformatted code? y/n: \n>")
                if user_input == 'y': 
                    print("Here is the raw code: \n")
                    code_block = extract_code(bot_message['content']) # Extracts the code from ChatGPT
                    print("\nRAW CODE: ", '\n', code_block, '\n', '\nBot-', bot_message['content']) # This is where ChatGPT responds and the code is logged into the console with the raw code included.
                elif user_input == 'n':
                    print(code_block, '\n', '\nBot-', bot_message['content']) # This is where ChatGPT responds and the code is logged into the console with the raw code excluded.
            user_input = input("\n>")
        else:
            user_input = input("\nNo response, try asking again.\n>")
    # Error handling
    except Exception as error:
        print(error)
        user_input = input("\nSomething went wrong, try asking again.\n>") 
