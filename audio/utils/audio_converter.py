import hashlib
import re
from pathlib import Path
from gtts import gTTS


def convert_text_to_speech(
    text: str,
    lang: str = "ko",
    slow: bool = False,
    __path: str = "audio/storage/",
) -> list[str]:
    """
    Split text by sentence and return file paths.
    """
    return [
        sentence_to_speech_fp(
            text=sentence,
            lang=lang,
            slow=slow,
            __path=__path,
        )
        for sentence in separate_text_by_sentence(text)
    ]


def sentence_to_speech_fp(
    text: str,
    lang: str = "ko",
    slow: bool = False,
    __path: str = "audio/storage/",
) -> str:
    """
    If speach file already exists, return file name.
    Else, create speach file and return file name.
    """
    file_name = (
        hashlib.sha256(  # create file name by hashing text
            text.encode("utf-8")
        ).hexdigest()
        + ("_slow" if slow else "")  # add "_slow" if slow sound
        + ".mp3"  # add file extension
    )
    file_path = Path(__path) / file_name[:6]
    Path.mkdir(Path(file_path), exist_ok=True)  # create path if not exist
    file_path /= file_name[6:]
    if file_path.exists():
        return file_path
    tts = gTTS(text=text, lang=lang, slow=slow)
    tts.save(file_path)
    return file_path


def separate_text_by_sentence(text: str) -> list:
    """
    Separate text by ".", "!", "?" and return list of sentences.
    """
    splits = re.split(r"(?![\.\!\?])(?<=[\.\!\?])\s*", text, flags=re.MULTILINE)
    # remove empty string
    without_empty_str = list(filter(None, splits))
    return without_empty_str
