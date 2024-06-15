### WIP ###
import logging
import os

from dotenv import load_dotenv

from db import SQLiteClient
from exceptions import NoRequiredVarEnv
from llm import (
    SpeechRecognizer,
    SpeechToText,
)

load_dotenv()

if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s: %(levelname)s - %(message)s - %(module)s",
        level=logging.INFO,
        datefmt="%d-%b-%y %H:%M:%S",
    )
    db_path: str | None = os.getenv("DB_PATH")
    if not db_path:
        raise NoRequiredVarEnv("DB_PATH")

    with SQLiteClient(db_path) as db:
        logging.info(db.get_random_notes(4))

    ai_api_key: str | None = os.getenv("WHISPER_API_KEY")
    if not ai_api_key:
        raise NoRequiredVarEnv("WHISPER_API_KEY")

    stt_client: SpeechToText = SpeechToText(ai_api_key)
    logging.info("%s initialized", stt_client.__class__.__name__)
    sr_client: SpeechRecognizer = SpeechRecognizer(stt_client)
    logging.info("%s initialized", sr_client.__class__.__name__)
    logging.info("Start listening")
    sr_client.start_listening(save_assets=True)
    while True:
        pass
