import os
import dotenv
dotenv.load_dotenv()

class config():
    def __init__(self):
        self.Telegram_API = os.getenv("Telegram_BOT_API_Key")
        self.OpenAI = os.getenv("OPENAI_API_KEY")
        self.News = os.getenv("news_api_key")
        self.WolframAlpha = os.getenv("WOLFRAM_ALPHA_APPID")
        self.Serpapi = os.getenv("SERPAPI_API_KEY")

config = config()
