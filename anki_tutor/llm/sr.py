import os
from datetime import datetime
from functools import partial
from typing import Any

import speech_recognition as sr  # type: ignore
from speech_recognition import (
    Microphone,
    Recognizer,
    audio,
)


class SoundWritingError(Exception):
    """Exception raised when error during saving WAF audio"""


class SpeechRecognizer:
    def __init__(self) -> None:
        self.recognizer: Recognizer = sr.Recognizer()
        self.microphone: Microphone = sr.Microphone()

    def _callback(
        self, save_sound: bool, _: Any, audio: audio.AudioData
    ) -> None:
        if save_sound:
            path_save_audio = "saved_audio"
            try:
                os.makedirs(path_save_audio, exist_ok=True)
                with open(
                    f"{path_save_audio}/{datetime.now().strftime("%m_%d %H_%M_%S_%f")}.wav",
                    "wb",
                ) as f:
                    f.write(audio.get_wav_data())
            except Exception as e:
                raise SoundWritingError("Error during saving WAF audio") from e

    def start_listening(self, save_sound: bool = True) -> None:
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
        self.recognizer.listen_in_background(
            self.microphone, partial(self._callback, save_sound)
        )
