# Python Voice Assistant

This project implements a **voice assistant** in Portuguese, capable of understanding and executing commands intelligently using natural language processing (NLP) and text-to-speech (TTS).

---

## Objective

Build a virtual assistant from scratch, featuring:

* **Wake word** (`assistente`) to activate listening.
* **Speech-to-Text** via the Google API using [`speech_recognition`](https://pypi.org/project/SpeechRecognition/).
* **Text-to-Speech** offline with [`pyttsx3`](https://pypi.org/project/pyttsx3/).
* Intuitive commands for:

  * YouTube and Google searches;
  * Location lookup and routes in Google Maps;
  * Current local time.

---

## 📁 Project Structure

```
assistente_virtual/
│
├── main.py                # Main loop and wake word handling
├── requirements.txt       # Project dependencies
└── modules/               # Package modules
    ├── __init__.py
    ├── tts.py             # Speech synthesis (pyttsx3)
    └── nlp_commands.py    # Intent recognition and action execution
```

---

## Technologies & Libraries

| Library           | Purpose                             |
| ----------------- | ----------------------------------- |
| Python 3.7+       | Core programming language           |
| SpeechRecognition | STT via Google API                  |
| PyAudio           | Microphone audio capture            |
| pyttsx3           | Offline TTS (Windows/macOS/Linux)   |
| geopy (Nominatim) | Geocoding via OpenStreetMap         |
| datetime          | Local date and time                 |
| re (regex)        | Command text parsing                |
| webbrowser        | Opening URLs in the default browser |

---

## How It Works

1. **Initialization**

   * Adjust ambient noise level to calibrate the recognizer.
2. **Main Loop**

   * Waits up to 3s for speech (`timeout`) and records up to 5s (`phrase_time_limit`).
   * If no speech is detected, repeats the loop without blocking.
   * Converts captured audio to text.
3. **Wake Word Detection**

   * Listens for `assistente` anywhere in the sentence.
   * If only the wake word is spoken, responds “Yes, how can I help?” and waits for the command.
4. **Intent Extraction**

   * **YouTube**: `video`, `assistir`, `youtube`
   * **Location**: “qual a localização de X”
   * **Distance/Route**: “qual a distância de X”
   * **Google**: “o que é X” / “quem é X” / “significado de X” / "pesquisar X" / "buscar X"
   * **Time**: “que horas são” / “horário” / “hora”
   * **Fallback**: the assistant asks to rephrase.
5. **Actions**

   * Opens YouTube, Google Search, or Google Maps URLs in the browser.
   * Speaks the response using `pyttsx3`.

---

## Usage Examples

```bash
python main.py
```

* “assistente pesquise Python” → opens a Google search for “Python”.
* “assistente vídeo sobre gatos” → opens a YouTube search for “gatos”.
* “assistente onde fica Curitiba” → opens Curitiba in Google Maps.
* “assistente o que é OpenAI” → opens a Google search for OpenAI.
* “assistente que horas são” → announces the current time.
* “assistente sair” → exits the assistant.

---

## Limitations

* **Online STT**: Requires Internet and the Google API.
* **Geocoding**: Also requires Internet and is rate-limited.
* **Speech Recognition**: Accuracy depends on microphone quality and background noise.
* **No Context Memory**: Each command is handled independently.

---

## Improvements & Suggestions

* Replace online STT with an offline solution (e.g., Vosk, PocketSphinx).
* Add weather, reminders, or integrate external APIs.
* Store conversation history for contextual awareness.
* Package as an installable Python module (`pip`).

---

## Contributions

Contributions are welcome!

```bash
git checkout -b feature-new-intent
# make changes
git commit -m "feat: add weather feature"
git push origin feature-new-intent
```

Then open a Pull Request.

---

## 📜 License

This project is licensed under the **MIT License**. See the `LICENSE` file for details.
