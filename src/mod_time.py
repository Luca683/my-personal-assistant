import datetime
import re
import importlib

master_module = importlib.import_module('master_module')


class ModuleTime(master_module.MasterModule):
    def __init__(self) -> None:
        self.time = False
        self.day = False
        self.date = False

    def check_command(self, command: str) -> bool:
        regex = r"\b(dimmi|dammi|che)\b.*\b(ora|ore|giorno|data)\b"
        if (re.search(regex, command)) is not None:
            if command.find("ora") != -1 or command.find("ore") != -1:
                self.time = True
            if command.find("giorno") != -1:
                print(command)
                self.day = True
            if command.find("data") != -1:
                self.date = True
                print(self.time)
            return True
        return False

    def execute(self, command: str) -> str:
        print(command)
        if self.time:
            now = datetime.datetime.now()
            current_time = now.strftime("Sono le : %H:%M")
            if self.day:
                d = datetime.datetime.now().strftime(" ed oggi è :%A")
                current_time += d
            return current_time
        if self.day:
            day = datetime.datetime.now().strftime("%A")
            print(day)
            return day
        if self.date:
            date = datetime.datetime.now().strftime('Oggi è :%A, %B %d, %Y')
            print(date)
            return date
        return "Specificami la data."
   