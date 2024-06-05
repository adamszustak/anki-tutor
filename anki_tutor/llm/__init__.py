import os

from .helper import BASE_DIR_FOR_SAVING
from .sr import SpeechRecognizer
from .stt import SpeechToText

os.makedirs(BASE_DIR_FOR_SAVING, exist_ok=True)
os.makedirs(
    f"{BASE_DIR_FOR_SAVING}/{SpeechRecognizer.PATH_TO_SAVE}", exist_ok=True
)
os.makedirs(
    f"{BASE_DIR_FOR_SAVING}/{SpeechToText.PATH_TO_SAVE}", exist_ok=True
)
