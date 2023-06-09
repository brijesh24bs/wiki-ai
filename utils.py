import os
from pathlib import Path
from dotenv  import load_dotenv
load_dotenv()


# Create folders if they don't exist
os.makedirs("data/", exist_ok=True)
os.makedirs("db/", exist_ok=True)
os.makedirs("models/", exist_ok=True)

