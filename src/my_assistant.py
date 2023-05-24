from pyttsx3 import init
import speech_recognition as sr
import sys
import os
import importlib

mod_volume = importlib.import_module('mod_volume')
mod_jokes = importlib.import_module('mod_jokes')
mod_time=importlib.import_module('mod_time')
mod_benchmark = importlib.import_module('mod_benchmark')
mod_testa_croce = importlib.import_module('mod_testa_croce')
master_module = importlib.import_module('master_module')

# Inizializzazione dell'assistente vocale + impostazione lingua italiana
try:
    reco = sr.Recognizer()
    micro = sr.Microphone()

    if sys.platform == 'Linux':
        engine = init()  # espeak
    elif sys.platform == 'darwin':
        engine = init(driverName='dummy')
    else: # sys.platform == 'win32':
        engine = init(driverName='sapi5')

    voices = engine.getProperty("voices")

    # Ricerca indice della lingua italiana nella lista "voices"
    italian_index = 0
    for index, item in enumerate(voices):
        if voices[index].id == "italian":
            italian_index = index
            break

    engine.setProperty("voice", voices[italian_index].id)

    hasMicrophone = True
except OSError:
    hasMicrophone = False
    print("Cannot define audio settings")

# Presa in input una stringa, questa verrà esposta a voce
def speak(response: str) -> None:
    if sys.platform == 'Linux':
        engine.say(response)
        engine.runAndWait()
    elif sys.platform == 'darwin':
        os.system(f"echo '{response}' | espeak -v it")

# Inseriamo il nostro comando (vocalmente), quindi questo verrà processato e convertito in una stringa
def input_command() -> str:
    try:
        with micro as source:
            print("pronto ad ascoltare...")
            audio = reco.listen(source)

        question = reco.recognize_google(audio, language="it-IT").lower()
    except NameError:
        question = "question_name_ex"
    except sr.UnknownValueError:
        question = "_NoQuestion"
    return question

# Funzione per stabilire quale modulo eseguire, ritorna quindi un'istanza del modulo interessato
def find_module(command: str) -> master_module.MasterModule:
    module_volume = mod_volume.ModuleVolume()
    module_jokes = mod_jokes.ModuleJokes()
    module_time = mod_time.ModuleTime()
    module_benchmark = mod_benchmark.ModuleBenchmark()
    module_testa_croce = mod_testa_croce.ModuleTestaCroce()

    if module_volume.check_command(command):
        return module_volume
    if module_jokes.check_command(command):
        return module_jokes
    if module_benchmark.check_command(command):
        return module_benchmark
    if module_time.check_command(command):
        return module_time
    if module_testa_croce.check_command(command):
        return module_testa_croce
    return None


def execute_command() -> bool:
    command = input_command()

    # Default value
    result = "Scusa, non so ancora come eseguire questo comando"
    flag = False

    # Quale comando deve essere eseguito?
    if command == "stop":
        flag = True
        result = "Alla prossima!"
    elif command == "_NoQuestion":
        result = "Scusa, non ho capito"
    else:
        module = find_module(command)
        if module is not None:
            result = module.execute(command)

    print(result)
    speak(result)
    return flag


if __name__ == "__main__":
    stop = False

    while not stop:
        stop = execute_command()
