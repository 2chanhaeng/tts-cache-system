import hashlib
import re
from pathlib import Path
from typing import Final
from gtts import gTTS

# Define default values
DEFAULT_LANG = "ko"
DEFAULT_PATH = "static/audio/"
DEFAULT_EXT = ".mp3"


def create_audio_file(
    text: str,
    speed: float = 1.0,
    path: str = DEFAULT_PATH,
    lang: str = DEFAULT_LANG,
    extension: str = DEFAULT_EXT,
) -> str:
    """
    If speach file already exists, return file name.
    Else, create speach file and return file name.
    """
    file_path: Final = get_file_path(text, speed, path, extension)
    if not file_path.exists():
        gTTS(text=text, lang=lang).save(file_path)


def get_file_path(
    text: str,
    speed: float = 1.0,
    path: str = DEFAULT_PATH,
    extension: str = DEFAULT_EXT,
) -> Path:
    """
    Define path by hashing text and name by hex code of speed.
    Default file name is /<path>/0x1.0000000000000p+0.<ext>
    """
    hashed: Final = hashlib.sha256(  # create file name by hashing text
        text.encode("utf-8")
    ).hexdigest()
    file_dir: Final = Path(path) / hashed[:6] / hashed[6:]
    Path.mkdir(Path(file_dir), exist_ok=True)  # create path if not exist
    file_path: Final = file_dir / speed.hex() + extension  # add speed to file name
    return file_path


def separate_text_by_sentence(text: str) -> list[str]:
    """
    Separate text by ".", "!", "?" and return list of sentences.
    """
    splits = re.split(r"(?![\.\!\?])(?<=[\.\!\?])\s*", text, flags=re.MULTILINE)
    # remove empty string
    without_empty_str = list(filter(None, splits))
    return without_empty_str
