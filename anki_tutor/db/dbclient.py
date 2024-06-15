from __future__ import annotations

import logging
import re
from collections.abc import Sequence
from dataclasses import dataclass
from sqlite3 import (
    Connection,
    Cursor,
    connect,
)
from typing import Any


@dataclass(frozen=True)
class Note:
    en_translation: str
    pl_translation: str
    en_sentences: tuple[str, ...]
    pl_sentences: tuple[str, ...]


class SQLiteClient:
    def __init__(self, db_path: str) -> None:
        self.connection: Connection
        self.cursor: Cursor
        self.db_path: str = db_path

    def __enter__(self) -> SQLiteClient:
        self.connection = connect(self.db_path)
        self.connection.set_trace_callback(logging.info)
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

    def get_random_notes(self, nr_of_notes: int = 5) -> list[Note]:
        """
        Retrieve a specified number of random notes from the Anki db that contain three occurrences of the delimiter '\x1f'. This indicates that the card is a standard card with sample sentences.
        Returns clean Note instances, with HTML tags removed.
        """
        results = self.execute_query(
            "SELECT flds from notes WHERE ( LENGTH(flds) - LENGTH(REPLACE(flds, '\x1f', '')) ) = 3 ORDER BY RANDOM() LIMIT ?",
            (nr_of_notes,),
        )
        # TODO: Add logic that will ensure nr_of_notes is achieved
        notes = []
        for result in results:
            raw_note = type(self).remove_html_tags(result[0]).replace(";", " ")
            en_translation, pl_translation, en_sentences, pl_sentences = (
                raw_note.split("\x1f")
            )

            en_examples = tuple(
                example for example in en_sentences.split("-") if example
            )
            pl_examples = tuple(
                example for example in pl_sentences.split("-") if example
            )
            note_input = (
                en_translation,
                pl_translation,
                en_examples,
                pl_examples,
            )
            if not all(note_input):
                logging.warning(
                    "Omit note (%s) due to lack some fields", note_input
                )
            notes.append(Note(*note_input))
        return notes

    @staticmethod
    def remove_html_tags(item: str) -> str:
        html_finder_re = "<.*?>"
        return re.sub(html_finder_re, "", item).replace("&nbsp", "")
