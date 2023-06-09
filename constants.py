import os
from chromadb.config import Settings

from dotenv import load_dotenv
load_dotenv()

PERSIST_DIRECTORY = os.environ.get('PERSIST_DIRECTORY')
CHROMA_SETTINGS = Settings(
    chroma_db_impl='duckdb+parquet',
    persist_directory=PERSIST_DIRECTORY,
    anonymized_telemetry=False
)