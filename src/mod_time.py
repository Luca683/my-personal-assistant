import datetime
import re
import importlib

master_module = importlib.import_module('master_module')

def convert_month(month: int) -> str:
    array_months = ["Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno", "Luglio", "Agosto", "Settembre", "Ottobre", "Novembre", "Dicembre"]
    return array_months[month-1]

def convert_week_day(day: str) -> str:
    array_english_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    array_italian_days = ["LunedÃ¬", "MartedÃ¬", "MercoledÃ¬", "GiovedÃ¬", "VenerdÃ¬", "Sabato", "Domenica"]
    return array_italian_days[array_english_days.index(day)]

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
        result = ''
        now = datetime.datetime.now() # now Ã¨ una stringa con giorno, data e ora di oggi
        if self.time:
            current_time = now.strftime("Sono le: %H:%M ")
            result += current_time
        if self.day:
            week_day = convert_week_day(now.strftime("%A"))
            current_day = "Oggi Ã¨: " + week_day + " "
            result += current_day
        if self.date:
            month = convert_month(now.month)
            current_date = now.strftime('Data: %d/'+month+'/%Y ')
            result += current_date
        print(result)
        return result
