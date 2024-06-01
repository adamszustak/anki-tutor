from __future__ import annotations

import re
from collections.abc import Sequence
from sqlite3 import (
    Connection,
    Cursor,
    connect,
)
from typing import Any


class NoRequiredDbParams(Exception):
    """Exception raised when required database parameters are missing."""


class SQLiteClient:
    def __init__(self, db_path: str) -> None:
        self.connection: Connection
        self.cursor: Cursor
        self.db_path: str = db_path

    def __enter__(self) -> SQLiteClient:
        self.connection = connect(self.db_path)
        self.cursor = self.connection.cursor()
        return self

    def __exit__(self, *args: Any) -> None:
        self.connection.close()

    def execute_query(
        self, query: str, params: Sequence[Any]
    ) -> list[tuple[str]]:
        self.cursor.execute(query, params)
        results = self.cursor.fetchall()
        return results

    def get_random_notes(self, nr_of_notes: int = 5) -> tuple[str, ...]:
        """
        Retrieve a specified number of random notes from the Anki db that contain three occurrences of the delimiter '\x1f'. This indicates that the card is a standard card with sample sentences.
        Returns clean records, with HTML tags removed.
        """
        results = self.execute_query(
            "SELECT flds from notes WHERE ( LENGTH(flds) - LENGTH(REPLACE(flds, '\x1f', '')) ) = 3 ORDER BY RANDOM() LIMIT ?",
            (nr_of_notes,),
        )
        return tuple(
            SQLiteClient.remove_html_tags(item[0]) for item in results
        )

    @staticmethod
    def remove_html_tags(item: str) -> str:
        html_finder_re = "<.*?>"
        return re.sub(html_finder_re, "", item).replace("&nbsp", "")
