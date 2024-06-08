from datetime import datetime
from functools import partial
from os import system
from typing import (
    Any,
    Final,
)

import speech_recognition as sr
from openai import OpenAI
from speech_recognition import (
    Microphone,
    Recognizer,
    audio,
)

from .helper import (
    BASE_DIR_FOR_SAVING,
    WAKEUP_KEYWORDS,
    AppController,
    SoundWritingError,
)


class SpeechRecognizer:
    PATH_TO_SAVE: Final[str] = "audio"

    def __init__(self, stt_client: OpenAI) -> None:
        self.recognizer: Recognizer = sr.Recognizer()
        self.microphone: Microphone = sr.Microphone()
        self.stt_client: OpenAI = stt_client

    def _callback(
        self, save_assets: bool, _: Any, audio: audio.AudioData
    ) -> None:
        controller: AppController = AppController()
        audio_wav: bytes = audio.get_wav_data()

        match controller:
            case AppController(True, _, _):
                self.listen_for_wake_word(audio_wav)

        if save_assets:
            file_name_to_save: str = (
                f"{datetime.now().strftime("%m_%d %H_%M_%S_%f")}"
            )
            self._save_audio_file(audio_wav, file_name_to_save)
            self.stt_client.transcribe(audio_wav, file_name_to_save)

    def _save_audio_file(
        self, audio_wav: bytes, file_name_to_save: str
    ) -> None:
        try:
            with open(
                f"{BASE_DIR_FOR_SAVING}/{self.PATH_TO_SAVE}/{file_name_to_save}.wav",
                "wb",
            ) as f:
                f.write(audio_wav)
        except Exception as e:
            raise SoundWritingError("Error during saving WAF audio") from e

    def listen_for_wake_word(self, audio_wav: bytes) -> None:
        transcription: str = self.stt_client.transcribe(audio_wav)
        if WAKEUP_KEYWORDS.SENTENCES.value in transcription.lower().strip():
            AppController(
                wait_for_wakeup=False,
                practise_sentences=True,
                practise_notes=False,
            )
            system(f"say '{WAKEUP_KEYWORDS.SENTENCES.value} launched'")
        elif WAKEUP_KEYWORDS.NOTES.value in transcription.lower().strip():
            AppController(
                wait_for_wakeup=False,
                practise_sentences=False,
                practise_notes=True,
            )
            system(f"say '{WAKEUP_KEYWORDS.NOTES.value} launched'")
        else:
            system(f"say 'Say again'")

    def start_listening(self, save_assets: bool = False) -> None:
        system("say 'How can i help you?'")
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
        self.recognizer.listen_in_background(
            self.microphone, partial(self._callback, save_assets)
        )
