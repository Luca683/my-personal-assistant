import re
import importlib
import psutil

master_module = importlib.import_module('master_module')


# Riceve valori nel formato xx.yyyy... oppure x.yyyy...
# Li restituisce nel formato xx.yy oppure x.yy
def formatPercentage(value: str) -> str:
    if len(value.split('.')[0]) < 2:
        return value[:4]

    return value[:5]


class ModuleBenchmark(master_module.MasterModule):
    def __init__(self):
        self.benchmark_cpu = False
        self.benchmark_ram = False
        self.benchmark_battery = False

    def check_command(self, command: str) -> bool:
        benchmark_regex = r"\b(benchmark|prestazioni)\b.*(?P<selector>\bsistema\b|\bprocessore\b|\bram|memoria\b|\bbatteria\b)"

        if (match := re.search(benchmark_regex, command)) is not None:
            # Se il selector restituisce la parola "sistema", allora inseriamo tutte le info nella risposta
            if match.group("selector") == "sistema":
                self.benchmark_cpu = True
                self.benchmark_ram = True
                self.benchmark_battery = True
            else:
                # La regex non riesce a catturare le singole parole, quindi ricerchiamole nella stringa
                if command.find(" processore") != -1:
                    self.benchmark_cpu = True
                if command.find(" ram") != -1 or command.find(" memoria") != -1:
                    self.benchmark_ram = True
                if command.find(" batteria") != -1:
                    self.benchmark_battery = True

            return True

        return False

    def execute(self, command: str) -> str:
        result = ''

        # CPU
        if self.benchmark_cpu:
            # Richiediamo la percentuale di utilizzo della cpu negli ultimi 4 secondi
            cpuPercent = str(psutil.cpu_percent(4))
            result += 'La percentuale di utilizzo della CPU è del ' + cpuPercent + ' percento, '

        # RAM
        if self.benchmark_ram:
            # psutil.virtual_memory() restituisce i seguenti dati
            # [memoria totale, memoria disponibile, percentauale di memoria usata, quantità di memoria usata, memoria libera]
            memPercent = str(psutil.virtual_memory()[2])
            memUsage = str(psutil.virtual_memory()[3] / 1000000000) # Convertiamo la memoria usata in Gb
            formattedRamUsage = formatPercentage(memUsage)
            result += 'la percentuale di utilizzo della RAM è del ' + memPercent + ' percento, '
            result += 'che ammonta a ' + formattedRamUsage + ' gigabyte utilizzati, '

        if self.benchmark_battery:
            # Restituisce [percentuale, secondi rimasti, alimentata]
            battery_info = psutil.sensors_battery()
            if battery_info:
                battery = str(battery_info[0])
                if battery_info[2]:
                    verb = 'd è'
                else:
                    verb = ' non è'
            else:
                battery = "0"
                verb = ' non è'

            result += 'la batteria è al ' + battery + ' percento, '
            result += 'e' + verb + ' alimentata'

        print(command)
        # print(result)

        return result
