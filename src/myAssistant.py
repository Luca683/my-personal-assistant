from pyttsx3 import init
import speech_recognition as sr

reco = sr.Recognizer()
micro = sr.Microphone()

engine = init()
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)

def speak(response) -> None:
    engine.say(response)
    engine.runAndWait()

def inputCommand() -> str | sr.UnknownValueError:
    with micro as source:
        #r.pause_threshold = 3.0
        print("pronto ad ascoltare...")
        audio = reco.listen(source)
    try:
        question = reco.recognize_google(audio, language="it-IT").lower()
        print(f"L'utente ha detto: {question}")
        return question
    except sr.UnknownValueError:
        print("Scusa non ho capito, puoi ripetere?")
        return sr.UnknownValueError

#if __name__ == "__main__":
#    stop = False
#    while stop==False:
#        inputCommand()
