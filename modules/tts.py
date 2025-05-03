import pyttsx3

_engine = pyttsx3.init()
_engine.setProperty('rate', 150)


def falar(texto: str):
    print(f"[TTS] {texto}")
    _engine.say(texto)
    _engine.runAndWait()