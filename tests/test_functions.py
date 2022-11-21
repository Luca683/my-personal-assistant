from src.myAssistant import *
import speech_recognition as sr 

def test_inputCommand_a() -> None: #try
    word_test = "ciao mondo"
    word_speak = inputCommand()
    assert word_test == word_speak
    
def test_inputCommand_b() -> None: #except
    word_speak = inputCommand()
    assert word_speak == sr.UnknownValueError     