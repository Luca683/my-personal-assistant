import re
import importlib
master_module = importlib.import_module('master_module')


class ModuleBenchmark(master_module.MasterModule):
    def __init__(self):
        self.benchmark_cpu = false
        self.benchmark_ram = false

    def check_command(self, command: str) -> bool:
        # update_regex = r"\b(?P<command>alza|abbassa)\b.*?\bvolume\b.+?\b(?P<selector>a|di)\b.+?\b(?P<value>\d+)\b"
        benchmark_regex = r"\b(benchmark|prestazioni)\b.*?\b(?P<value>tutt(i|o))*.*?((?P<system>sistema)|(?P<cpu>cpu)|(?P<ram>ram|memoria))+"gi

        if (match := re.search(update_regex, command)) is not None:
            value = int(match.group("value"))
            self.value = clamp_val(value)
            self.is_to = match.group("selector") == "a"
            self.is_by = not self.is_to
            self.action_update = True
            return True

        return False

    def execute(self, command: str) -> str:


        return "Ho modificato il volume"
