import re
import random
import importlib

master_module = importlib.import_module('master_module')

class ModuleTestaCroce(master_module.MasterModule):
    def __init__(self):
        pass

    def check_command(self, command):
        first_regex = r"(lancia|tira)\s?(la|una)?\s?moneta" #Stringhe del tipo "lancia(tira) una(la) moneta"
        second_regex = r"(giochiamo\s+a\s+)?(testa\s+o\s+croce|croce\s+o\s+testa)" #Stringhe del tipo "giochiamo a testa o croce" o "testa o croce"
        if(re.search(first_regex, command) or re.search(second_regex, command)):
            return True
        return False

    def execute(self, command):
        print("Eseguo comando: "+command)
        moneta = random.randint(0, 1) # 0 = Testa, 1 = Croce
        if moneta==0:
            return "E' uscito testa"
        return "E' uscito croce"
