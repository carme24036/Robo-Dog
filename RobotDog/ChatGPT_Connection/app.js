// This is the original Javascript version of the ChatGPT-RoboDog project.

// import modules
import { stdin as input, stdout as output } from "node:process";          // Used to interact with the command line or console 
import { createInterface } from "node:readline/promises";                 // Used to read lines of text from an input source like the command line
const readline = createInterface({ input, output });                      // Allows the program to read text from an input source and write text to an output source
import * as dotenv from "dotenv";                                         // Allows the program to read content from environmental variables
dotenv.config();

import OpenAI from 'openai';
const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY                                      // Gets openai API key from the .env file for use in this program
});

// import the go1 js node library and initialize the Robot Dog
import { Go1, Go1Mode } from "@droneblocks/go1-js";
let dog = new Go1();
dog.init();
dog.setMode(Go1Mode.stand);
// dog.goForward(0.25, 2000);                                               This is commented because otherwise it will make the dog move as soon as the program is run

// This function will only be used when ChatGPT sends a response that involves code. It extracts code blocks from ChatGPT's response
const extractJSCode = (content) => {
  const regex = /```([^\n]*)\n([\s\S]*?)```/g;
  const matches = [...content.matchAll(regex)];
  const codeBlocks = matches.map((match) => ({
    language: 'javascript',
    codeBlock: match[2].trim(),
  }));
  return codeBlocks;
};

// This is the initial message that is sent to ChatGPT when the program is run. It tells ChatGPT how to control the robot dog so that it can make programs from it. 
const chatPrompt = `
Hello ChatGPT. You are going to be helping me control the Unitree Go1 Robot Dog. 
Here are some method definitions to control the Go1:
                    
  goForward(speed: number, lengthOfTime: number)
  goBackward(speed: number, lengthOfTime: number)
  goLeft(speed: number, lengthOfTime: number)
  goRight(speed: number, lengthOfTime: number)
  turnLeft(speed: number, lengthOfTime: number)
  turnRight(speed: number, lengthOfTime: number)
  
All methods accept two arguments the first is speed with a value from 0 to 1, where 1 is full speed. The second argument is a duration in milliseconds.

Keep in mind that before we can move Go1, we need to make sure to set it's mode to Go1Mode.walk.

There is a wait method in cases where we want to pause between commands. It accepts a number in milliseconds:

  wait(lengthOfTime: number)

Please make sure that all wait commands are awaited.

For the dog to lay down we use the following command:

  setMode(Go1Mode.standDown)

and to stand up we use

  setMode(Go1Mode.standUp)

You can also change the LEDs of the robot dog using the following commands:

  setLedColor(red: number, green: number, blue: number)

Where red, green, and blue are integers between 0 and 255.

Blinking the LED must always have a 2 second delay between colors.

For this program, make sure the code is in Javascript.
`;

// This variable is what keeps track of what messages were sent to ChatGPT from the user and recieved from ChatGPT to the user
const messages = [{ role: "system", content: chatPrompt }];

let userInput = await readline.question("Welcome to ChatGPT. Feel free to ask questions. To exit the program, type 'quit' or ctrl + c.\n\n>")

let botMessage; // ChatGPT's response/message

while (userInput != "quit") {
  messages.push({ role: "user", content: userInput });

  try {
    const chatCompletion = await openai.chat.completions.create({
      messages,
      model: "gpt-3.5-turbo",
    });

    botMessage = chatCompletion.choices[0].message;

    if (botMessage) {
      messages.push(botMessage);
      const codeBlock = extractJSCode(botMessage.content);                              //Extracts the code from ChatGPT
      console.log("\nRAW CODE: ", '\n', codeBlock, '\n', "\nBot-", botMessage.content); // This is where ChatGPT responds and the code is logged into the console.
      userInput = await readline.question("\n>");
    }
    else {
      userInput = await readline.question("\nNo response, try asking again.\n>");
    };
  }
  // Error handling
  catch (error) {
    console.log(error.message);
    userInput = await readline.question("\nSomething went wrong, try asking again.\n>");
  };
  readline.close();
};

