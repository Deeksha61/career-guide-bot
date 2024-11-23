# config.py
import os
from dotenv import load_dotenv


# Load environment variables
load_dotenv()

class Config:
    # API Configuration
    MONSTER_API_KEY = os.getenv("MONSTER_API_KEY")
    MONSTER_API_URL = "https://api.monster.com/jobs/search"
    
    # Backend API Configuration
    BACKEND_URL = "http://localhost:8000"
    
    # NLP Configuration
    SPACY_MODEL = "en_core_web_sm"
    
    # Database Configuration
    SKILLS_DB_PATH = "skills_database.json"
    
    # API Rate Limiting
    MAX_REQUESTS_PER_MINUTE = 60
    
    # Job Search Configuration
    DEFAULT_LOCATION = "United States"
    DEFAULT_JOB_LIMIT = 10
    
    # Skill Analysis Configuration
    MIN_SKILL_FREQUENCY = 2
    MAX_SKILLS_PER_CATEGORY = 5