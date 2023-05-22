from pyttsx3 import init
import speech_recognition as sr

import importlib
mod_volume = importlib.import_module('mod_volume')
mod_jokes = importlib.import_module('mod_jokes')
mod_time=importlib.import_module('mod_time')
mod_benchmark = importlib.import_module('mod_benchmark')
mod_testa_croce = importlib.import_module('mod_testa_croce')
master_module = importlib.import_module('master_module')


try:
    reco = sr.Recognizer()
    micro = sr.Microphone()

    engine = init()
    voices = engine.getProperty("voices")

    #search index of italian language in list "voices"
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

def speak(response) -> None:
    engine.say(response)
    engine.runAndWait()


def inputCommand() -> str:
    try:
        with micro as source:
            # r.pause_threshold = 3.0
            print("pronto ad ascoltare...")
            audio = reco.listen(source)

        question = reco.recognize_google(audio, language="it-IT").lower()
    except NameError:
        question = "question_name_ex"
    except sr.UnknownValueError:
        question = "_NoQuestion"
    return question


def findModule(command: str) -> master_module.MasterModule:
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


def execute() -> bool:
    command = inputCommand()

    #Default value
    result = "Scusa, non so ancora come eseguire questo comando"
    flag = False

    if command == "stop":
        flag = True
        result = "Alla prossima!"
    elif command == "_NoQuestion":
        result = "Scusa, non ho capito"
    else:
        module = findModule(command)
        if module is not None:
            result = module.execute(command)

    print(result)
    speak(result)
    return flag


if __name__ == "__main__":
    stop = False

    while not stop:
        stop = execute()
