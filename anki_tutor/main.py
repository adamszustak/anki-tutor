### WIP ###
import os

from db import (
    NoRequiredDbParams,
    SQLiteClient,
)
from dotenv import load_dotenv  # type: ignore
from llm import (
    NoRequiredAPIKey,
    SpeechRecognizer,
    SpeechToText,
)

load_dotenv()

if __name__ == "__main__":
    db_path: str | None = os.getenv("DB_PATH")
    if not db_path:
        raise NoRequiredDbParams(
            "Script cannot find required environment variable DB_PATH."
        )

    with SQLiteClient(db_path) as db:
        print(db.get_random_notes(4))

    ai_api_key: str | None = os.getenv("WHISPER_API_KEY")
    if not ai_api_key:
        raise NoRequiredAPIKey(
            "Script cannot find required environment variable WHISPER_API_KEY."
        )

    stt_client: SpeechToText = SpeechToText(ai_api_key)
    sr_client: SpeechRecognizer = SpeechRecognizer(stt_client)
    sr_client.start_listening(save_assets=True)
    while True:
        pass
