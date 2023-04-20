import re
import importlib
import psutil
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
    
    def formatPercentage(self, value) -> str:
        if len(value.split('.')[0]) < 2:
            return value[:4]
        else:
            return value[:5]


    def execute(self, command: str) -> str:
        result = ''

        # CPU
        if self.benchmark_cpu:
            cpuPercent = str(psutil.cpu_percent(4))
            result += 'La percentuale di utilizzo della CPU è del ' + cpuPercent + ' percento, '

        # RAM
        if self.benchmark_ram:
            memPercent = str(psutil.virtual_memory()[2])
            memUsage = str(str(psutil.virtual_memory()[3]/1000000000))   
            formattedRamUsage = self.formatPercentage(memUsage)
            result += 'la percentuale di utilizzo della RAM è del ' + memPercent + ' percento, '
            result += 'che ammonta a ' + formattedRamUsage + ' gigabyte utilizzati, '
        
        if self.benchmark_battery:
            battery = str(psutil.sensors_battery()[0])

            if psutil.sensors_battery()[2]:
                verb = 'd è'
            verb = ' non è'
        
            result += 'la batteria è al ' + battery + ' percento, '
            result += 'e' + verb + ' alimentata'

        print(result)

        return result
