import re
import importlib
import pyjokes

master_module = importlib.import_module('master_module')


class ModuleJokes(master_module.MasterModule):
    def __init__(self) -> None:
        self.lang = "it"

    def check_command(self, command: str) -> bool:
        regex = r"\b(raccontami|fammi|dimmi)\b.*?\b(barzelletta|battuta)\b.*?(\b(?P<lingua>inglese|tedesco|spagnolo)\b)*$"
        print("check")
        _match = re.search(regex, command)
        if _match is not None:
            print(_match.group("lingua"))
            if _match.group("lingua") == "inglese":
                self.lang = "en"
            elif _match.group("lingua") == "tedesco":
                self.lang = "de"
            elif _match.group("lingua") == "spagnolo":
                self.lang = "es"
            return True

        return False

    def execute(self, command: str) -> str:
        print(command)
        return pyjokes.get_joke(language=self.lang)
