import os
import re
import telebot
import translators as ts
from config import config
from langchain.llms import OpenAI
from langchain.agents import load_tools, initialize_agent
from langchain.chains.conversation.memory import ConversationBufferMemory

# API Key for OpenAI
os.environ["OPENAI_API_KEY"] = config.OpenAI


# API Key for Telegram bot
bot = telebot.TeleBot(config.Telegram_API)


# Create an instance of the language model with OpenAI temperature set to the middle for variety
roboroc = OpenAI(temperature=0.5)


# Create a function that performs a specific duty and memory to the conversation
tools = load_tools(["serpapi", "open-meteo-api", "news-api", "wolfram-alpha"], llm=roboroc,
                   WOLFRAM_ALPHA_APPID=config.WolframAlpha, news_api_key=config.News, serpapi_api_key=config.Serpapi)
memory = ConversationBufferMemory(memory_key="chat_history")


# Create the agent which uses the tools
agent = initialize_agent(tools, roboroc, agent="conversational-react-description", memory=memory, verbose=True)


# Telegram initialization command
@bot.message_handler(commands=["Dorele"])
def reply(message):
    bot.reply_to(message, "Salut! Cu ce te pot ajuta?")


def call_request(message):  # function to allow us to call the bot without the initialization command
    request = message.text.split("!")
    if bool(re.search("Bai\s*Dorele\s*", request[0])):  # when this will be written, will give signal to next function
        return True
    else:
        return False


@bot.message_handler(func=call_request)
def another_reply(message):  # read the message and answer to chat with the help of the agent
    request = message.text.split("!")
    # translate from romanian to eng and vice versa
    bot.reply_to(message, ts.translate_text(query_text=agent.run
    (input=ts.translate_text(query_text=request[1], to_language="en")), to_language="ro"))


bot.polling()