from pyttsx3 import init
import speech_recognition as sr

import mod_volume

reco = sr.Recognizer()
micro = sr.Microphone()

engine = init()
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)


def speak(response) -> None:
    engine.say(response)
    engine.runAndWait()


def inputCommand() -> str:
    with micro as source:
        # r.pause_threshold = 3.0
        print("pronto ad ascoltare...")
        audio = reco.listen(source)

    question = reco.recognize_google(audio, language="it-IT").lower()
    return question


if __name__ == "__main__":
    stop = False

    while not stop:
        try:
            command = inputCommand().lower()
            print("Lettura finita")
        except sr.UnknownValueError:
            speak("Scusa non ho capito, puoi ripetere?")
            continue

        print("Ecco cosa ho sentito")
        print(command)
        speak("Ecco cosa ho sentito")
        speak(command)

        result = "Scusa, non so ancora come eseguire questo comando"

        if command == "stop":
            stop = True
            result = "Alla prossima!"

        elif mod_volume.check_command(command):
            result = mod_volume.execute(command)

        # Chain HERE "elif" for each module

        speak(result)
