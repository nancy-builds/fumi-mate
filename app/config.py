
import os
from dotenv import load_dotenv
load_dotenv()


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY') or 'dev'
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    OPENAI_MODEL = os.getenv('OPENAI_MODEL')
    OPENAI_EMBED_MODEL = os.getenv('OPENAI_EMBED_MODEL')
    CHROMA_DIR = os.getenv('CHROMA_DIR', './chroma_db')
    DEFAULT_JLPT_LEVEL = os.getenv('DEFAULT_JLPT_LEVEL','N5')


config = Config()