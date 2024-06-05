from typing import Final

BASE_DIR_FOR_SAVING: Final[str] = "saved_assets"


class SoundWritingError(Exception):
    """Exception raised when error during saving WAF audio"""


class TextWritingError(Exception):
    """Exception raised when error during saving text file"""


class NoRequiredAPIKey(Exception):
    """Exception raised when required API KEY parameter is missing."""
