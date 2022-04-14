import json
import os
f = open ("secret.json", "r")
secret= json.loads(f.read())

class Settings:
    PROJECT_NAME:str = "COLIBRI"
    PROJECT_VERSION: str = "1.0.0"
    POSTGRES_USER : str = secret["POSTGRES_USER"]
    POSTGRES_PASSWORD:str =secret["POSTGRES_PASSWORD"] 
    POSTGRES_SERVER : str=secret["POSTGRES_SERVER"]
    POSTGRES_PORT :str=secret['POSTGRES_PORT']
    POSTGRES_DB :str=secret["POSTGRES_DB"]
    DATABASE_URL = f"postgres://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"

settings = Settings()