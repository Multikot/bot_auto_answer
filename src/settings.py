from pydantic import BaseSettings
from dotenv import load_dotenv


class Settings(BaseSettings):

    api_id: int
    api_hash: str
    self_user_id: int
    self_chat_id: int
    message_answer: str

    class Config:
        load_dotenv()
        env_file = ('.env')
        env_file_encoding = 'utf-8'
