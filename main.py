import os
import sys
import time
import speech_recognition as sr

sys.path.insert(0, os.path.abspath(os.getcwd()))
from modules.tts import falar
from modules.nlp_commands import executar_comando

WAKE_WORDS = ["assistente", "oi assistente", "hey assistente"]
STOP_WORDS = ["sair", "tchau", "adeus"]

def extrair_comando(frase: str) -> str:
    frase = frase.lower().strip()
    for w in WAKE_WORDS:
        if w in frase:
            return frase.split(w, 1)[1].strip(" ,:.–-")
    return ""

def main():
    rec = sr.Recognizer()
    mic = sr.Microphone()

    # Ajuste inicial para ruído ambiente
    with mic as source:
        rec.adjust_for_ambient_noise(source, duration=1)
        print("Microfone ajustado. Diga ‘assistente’ seguido do comando.")

        while True:
            
            try:
                # aguarda até 3s por algo parecido com fala, captura até 5s de áudio
                audio = rec.listen(source, timeout=3, phrase_time_limit=5)
            except sr.WaitTimeoutError:
                # não ouvi nada nesse intervalo, continua o loop
                continue

            try:
                frase = rec.recognize_google(audio, language="pt-BR")
                print(f"[DEBUG] frase completa: '{frase}'")
            except Exception:
                # if recognition fails, volta a esperar
                continue

            cmd = extrair_comando(frase)
            if not cmd:
                # Sem wake-word, ignora
                continue

            if cmd == "":
                # Apenas wake-word: pede o comando
                falar("Sim, em que posso ajudar?")
                try:
                    audio2 = rec.listen(source, timeout=3, phrase_time_limit=5)
                except sr.WaitTimeoutError:
                    falar("Nenhum comando recebido.")
                    continue

                try:
                    cmd = rec.recognize_google(audio2, language="pt-BR").lower().strip()
                    print(f"[DEBUG] comando pós-prompt: '{cmd}'")
                except Exception:
                    falar("Não entendi, pode repetir?")
                    continue

            # Comando de saída
            if any(sw in cmd for sw in STOP_WORDS):
                falar("Até mais!")
                break

            print(f"[DEBUG] executando comando: '{cmd}'")
            executar_comando(cmd)
            print("Aguardando seu comando...")
            time.sleep(0.5)

    print("Assistente finalizado.")

if __name__ == "__main__":
    main()
