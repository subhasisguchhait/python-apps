import os
from dotenv import load_dotenv


abs_path=os.path.abspath(os.path.dirname(__file__))
path=os.path.join(abs_path, 'config.env')
# print(f"Loading environment variables from: {path}")
load_dotenv(path)

class Settings:
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
    JWT_SECRET = os.environ.get("JWT_SECRET", "dev-secret")
    JWT_ISSUER = os.environ.get("JWT_ISSUER", "robolibrarian")

    # Models (choose any available ones in your account)
    CHAT_MODEL = "gpt-4o-mini"          # simple + cheap
    EMBED_MODEL = "text-embedding-3-small"

settings = Settings()
print("Configuration loaded successfully.")
print(settings.OPENAI_API_KEY[-5:] + "..." )  # Print last 5 chars for verification