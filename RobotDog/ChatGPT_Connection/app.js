// import modules
import { stdin as input, stdout as output } from "node:process";
import { createInterface } from "node:readline/promises";
const readline = createInterface({ input, output });
import * as dotenv from "dotenv";
dotenv.config();

import OpenAI from 'openai';
const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

// import the go1 js node library to use with the robot dog
import { Go1, Go1Mode } from "@droneblocks/go1-js";
let dog = new Go1();
dog.init();
dog.setMode(Go1Mode.stand);
// dog.goForward(0.25, 2000);

// This will only be used when code is involved. 
const extractJSCode = (content) => {
  const regex = /```([^\n]*)\n([\s\S]*?)```/g;
  const matches = [...content.matchAll(regex)];
  const codeBlocks = matches.map((match) => ({
    language: match[1].trim(),
    codeBlock: match[2].trim(),
  }));
  return codeBlocks;
};

// This is a message that is sent to ChatGPT when the program is run. It is telling it how to control the robot dog. 
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

`;

const messages = [{ role: "system", content: chatPrompt }];
let userInput = await readline.question("Welcome to ChatGPT. Feel free to ask it questions. \n>")

let botMessage;

while (userInput !== "quit") {

  messages.push({ role: "user", content: userInput });

  try {
    const chatCompletion = await openai.chat.completions.create({
      messages,
      model: "gpt-3.5-turbo",
    });

    botMessage = chatCompletion.choices[0].message;

    if (botMessage) {
      messages.push(botMessage)

      const codeBlock = extractJSCode(botMessage.content)
    
      console.log("\n", botMessage.content, "\n")

      userInput = await readline.question("\n>")

    } else {
      userInput = await readline.question("\nNo response, try asking again.\n>");
    }
  } catch (error) {
    console.log(error.message);
    userInput = await readline.question("\nSomething went wrong, try asking again.\n>");
  };
};

readline.close();
