# Import modules
import os                        # Works with env stuff (I think)
import openai                    # OpenAI module needed to communicate with ChatGPT API
from dotenv import load_dotenv   # Lets the program load/read .env files
import re                        # Support for regular expressions

# Load environment variables from a .env file
load_dotenv()

# Initialize OpenAI client
api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = api_key

# Function to extract code blocks 
def extract_code(content):
    regex = r"```([^\n]*)\n([\s\S]*?)```"
    matches = re.finditer(regex, content)
    code_blocks = [{"language": match.group(1).strip(), "code_block": match.group(2).strip()} for match in matches]
    return code_blocks

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

That code adds a path to the Python library.

The following code is what will get the dog to walk:

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
        cmd.gaitType = 0
        cmd.speedLevel = 0         # This controls the level of speed
        cmd.footRaiseHeight = 0    # This is how high the foot of the dog is raised
        cmd.bodyHeight = 0         # This changes the height of the dog's body
        cmd.euler = [0, 0, 0]
        cmd.velocity = [0, 0]      # This is what controls the velocity/speed
        cmd.yawSpeed = 0.0
        cmd.reserve = 0

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
"""

messages = [{"role": "system", "content": chat_prompt}]
user_input = input("Welcome to ChatGPT. Feel free to ask questions. To exit the program, type 'quit'.\n\n> ")

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
        user_input = input("\nSomething went wrong, try asking again.\n>") 
