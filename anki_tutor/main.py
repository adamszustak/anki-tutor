### WIP ###
import os

from db import (
    NoRequiredDbParams,
    SQLiteClient,
)
from dotenv import load_dotenv  # type: ignore
from llm import SpeechRecognizer

load_dotenv()
db_path: str | None = os.getenv("DB_PATH")
if not db_path:
    raise NoRequiredDbParams(
        "Script cannot find required environment variable DB_PATH."
    )

with SQLiteClient(db_path) as db:
    print(db.get_random_notes(4))


open_ai_key: str | None = os.getenv("WHISPER_API_KEY")
if not db_path:
    raise NoRequiredDbParams(
        "Script cannot find required environment variable DB_PATH."
    )
s = SpeechRecognizer()
s.start_listening()
try:
    while True:
        pass
except KeyboardInterrupt:
    print("Stopped listening.")
