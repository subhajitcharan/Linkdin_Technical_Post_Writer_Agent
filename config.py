from pydantic_settings import BaseSettings,SettingsConfigDict
class Settings(BaseSettings):
    MODEL:str
    API_KEY:str
    LANGSMITH_ENDPOINT:str
    LANGSMITH_API_KEY:str
    LANGSMITH_PROJECT:str
    LANGSMITH_TRACING:str
    model_config=SettingsConfigDict(env_file='.env', extra='allow')
settings=Settings()