# core/config.py
import os
from dotenv import load_dotenv

# Load the .env file from the project's root directory
load_dotenv()

class Settings:
    """A class to hold all application settings loaded from the environment."""
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    SLACK_BOT_TOKEN: str = os.getenv("SLACK_BOT_TOKEN")
    SLACK_SIGNING_SECRET: str = os.getenv("SLACK_SIGNING_SECRET")
    SLACK_ESCALATION_USER_ID: str = os.getenv("SLACK_ESCALATION_USER_ID")
    PIPEDRIVE_API_URL: str = os.getenv("PIPEDRIVE_API_URL")
    PIPEDRIVE_API_KEY: str = os.getenv("PIPEDRIVE_API_KEY")

# Create a single, accessible instance of the settings
settings = Settings()