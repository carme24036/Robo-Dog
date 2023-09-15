import { stdin as input, stdout as output} from "node:process";
import { createInterface } from "node:readline/promises";
const readline = createInterface({ input, output });
import * as dotenv from "dotenv";
dotenv.config();

import OpenAI from 'openai';

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY, 
});

const extractJSCode = (content) => {
  const regex = /```([^\n]*)\n([\s\S]*?)```/g;
  const matches = [...content.matchAll(regex)];
  const codeBlocks = matches.map((match) => ({
    language: match[1].trim(),
    codeBlock: match[2].trim(),
  }));
  return codeBlocks;
};

const chatPrompt = "Hello, how may I help you?";
const messages = [{ role: "system", content: chatPrompt }];
let userInput = await readline.question("> ")

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

      console.log(botMessage.content)

      userInput = await readline.question("\nFeel free to ask another question:\n>")

    } else {
      userInput = await readline.question("\nNo response, try asking again\n");
    }
  } catch (error) {
    console.log(error.message);
    userInput = await readline.question("\nSomething went wrong, try asking again\n");
  };
};

readline.close();
