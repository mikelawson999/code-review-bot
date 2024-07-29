import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    MAX_TOKENS = int(os.getenv('MAX_TOKENS', 150))
    TEMPERATURE = float(os.getenv('TEMPERATURE', 0.5))
    REPO_URL = os.getenv('REPO_URL')
    GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
