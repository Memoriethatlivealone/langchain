from dotenv import load_dotenv
import os
import openai
print(openai.__version__)
load_dotenv()
api_key=os.getenv("OPENAI_API_KEY")
print(api_key)