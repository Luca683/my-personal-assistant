import re
import importlib
master_module = importlib.import_module('master_module')


class ModuleBenchmark(master_module.MasterModule):
    def __init__(self):
        self.benchmark_cpu = False
        self.benchmark_ram = False
        self.benchmark_battery = False

    def check_command(self, command: str) -> bool:
        benchmark_regex = r"\b(benchmark|prestazioni)\b.*(\b(?P<sys>sistema)\b|\b(?P<cpu>cpu)\b|\b(?P<ram>ram|memoria)\b|\b(?P<bat>batteria)\b)"

        if (match := re.search(benchmark_regex, command)) is not None:
            if match.group("sys") == "sistema":
                self.benchmark_cpu = True
                self.benchmark_ram = True
                self.benchmark_battery = True
            else:
                if match.group("cpu") == "cpu":
                    self.benchmark_cpu = True
                if match.group("ram") == "ram":
                    self.benchmark_ram = True
                if match.group("bat") == "batteria":
                    self.benchmark_battery = True
            
            return True

        return False

    def execute(self, command: str) -> str:


        return "Ho modificato il volume"
