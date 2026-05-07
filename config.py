import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not DISCORD_TOKEN:
    print("Warning: DISCORD_TOKEN not found in environment variables.")
if not GEMINI_API_KEY:
    print("Warning: GEMINI_API_KEY not found in environment variables.")
