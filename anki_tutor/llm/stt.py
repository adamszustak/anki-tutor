from io import BytesIO
from typing import Final

from openai import OpenAI

from .helper import (
    BASE_DIR_FOR_SAVING,
    TextWritingError,
)


class SpeechToText:
    PATH_TO_SAVE: Final[str] = "text"

    def __init__(self, api_key: str) -> None:
        self.client: OpenAI = OpenAI(api_key=api_key)

    def transcribe(
        self, audio: bytes, file_name_to_save: str | None = None
    ) -> str:
        audio_data = BytesIO(audio)
        audio_data.name = "SpeechRecognition_audio.wav"
        transcription: str = self.client.audio.transcriptions.create(
            model="whisper-1", file=audio_data, language="en"
        ).text
        if file_name_to_save:
            self._save_text_file(transcription, file_name_to_save)
        return transcription

    def _save_text_file(self, content: str, file_name_to_save: str) -> None:
        try:
            with open(
                f"{BASE_DIR_FOR_SAVING}/{self.PATH_TO_SAVE}/{file_name_to_save}",
                "w",
                encoding="utf-8",
            ) as f:
                f.write(content)
        except Exception as e:
            raise TextWritingError("Error during saving WAF audio") from e
