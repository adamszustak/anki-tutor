import os

from db import (
    NoRequiredDbParams,
    SQLiteClient,
)
from dotenv import load_dotenv  # type: ignore

load_dotenv()
db_path: str | None = os.getenv("DB_PATH")
if not db_path:
    raise NoRequiredDbParams(
        "Script cannot find required environment variable DB_PATH."
    )


with SQLiteClient(db_path) as db:
    print(db.get_random_notes(4))
