from __future__ import annotations

from enum import (
    Enum,
    auto,
)
from typing import (
    Any,
    Final,
    Iterator,
)

BASE_DIR_FOR_SAVING: Final[str] = "saved_assets"


class SoundWritingError(Exception):
    """Exception raised when error during saving WAF audio"""


class TextWritingError(Exception):
    """Exception raised when error during saving text file"""


class WAKEUP_KEYWORDS(Enum):
    @staticmethod
    def _generate_next_value_(name: str, *args: Any) -> str:
        return name.lower()

    SENTENCES = auto()
    NOTES = auto()


class AppController:
    _instance: AppController | None = None
    __match_args__ = (
        "wait_for_wakeup",
        "practise_sentences",
        "practise_notes",
    )

    def __new__(cls, *args, **kwargs) -> AppController:  # type: ignore
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init()
        else:
            cls._instance._update(*args, **kwargs)
        return cls._instance

    def _init(self) -> None:
        self.wait_for_wakeup: bool = True
        self.practise_sentences: bool = False
        self.practise_notes: bool = False

    def _update(
        self,
        wait_for_wakeup: bool | None = None,
        practise_sentences: bool | None = None,
        practise_notes: bool | None = None,
    ) -> None:
        if wait_for_wakeup is not None:
            self.wait_for_wakeup = wait_for_wakeup
        if practise_sentences is not None:
            self.practise_sentences = practise_sentences
        if practise_notes is not None:
            self.practise_notes = practise_notes

    def __str__(self) -> str:
        return f"{self.__class__.__name__} -> wait_for_wakeup: {self.wait_for_wakeup}, practise_sentences: {self.practise_sentences}, practise_notes: {self.practise_notes}"

    def __repr__(self) -> str:
        return f"{type(self).__name__}({tuple(self)})"

    def __iter__(self) -> Iterator[bool]:
        return (
            a
            for a in (
                self.wait_for_wakeup,
                self.practise_sentences,
                self.practise_notes,
            )
        )
