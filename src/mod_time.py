import datetime
import re
import importlib
import pyjokes

master_module = importlib.import_module('master_module')


class ModuleTime(master_module.MasterModule):
    def __init__(self) -> None:
        self.lang = "it"

    def check_command(self, command: str) -> bool:
        regex = r"\b(ore|ora|oggi)\b."
        print("check")
        if (match := re.search(regex, command)) is not None:
            return True
        return False

    def execute(self, command: str) -> str:
        print(command)
        now = datetime.datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print(current_time)
        return current_time
      
