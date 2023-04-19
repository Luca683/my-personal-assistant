import re
import importlib
master_module = importlib.import_module('master_module')


class ModuleBenchmark(master_module.MasterModule):
    def __init__(self):
        self.benchmark_cpu = False
        self.benchmark_ram = False

    def check_command(self, command: str) -> bool:
        # update_regex = r"\b(?P<command>alza|abbassa)\b.*?\bvolume\b.+?\b(?P<selector>a|di)\b.+?\b(?P<value>\d+)\b"
        benchmark_regex = r"\b(benchmark|prestazioni)\b.*?(?P<system>(sistema|cpu|ram|memoria))+"

        if (match := re.search(benchmark_regex, command)) is not None:
            if match.group("system") == "sistema":
                self.benchmark_cpu = True
                self.benchmark_ram = True
            elif match.group("system") == "cpu":
                self.benchmark_cpu = True
            elif match.group("system") == "ram":
                self.benchmark_ram = True
            
            return True

        return False

    def execute(self, command: str) -> str:


        return "Ho modificato il volume"
