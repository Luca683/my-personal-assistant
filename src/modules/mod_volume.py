from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from .master_module import MasterModule
import re


# Clamp values between 0 and 100
def clamp_val(number: int) -> int:
    if number < 0:
        return 0
    elif number > 100:
        return 100

    return number


# Returns the first digital occurrence in the command, or -1 if it not exists
def retrieve_number_in_string(string: str) -> int:
    number = ""
    flag = 0
    for w in string:
        if w.isdigit():
            number += w
            flag = 1
        elif flag == 1:
            break

    if number == "":
        return -1

    return clamp_val(int(number))


class ModuleVolume(MasterModule):
    def __init__(self):
        self.action_set = False
        self.is_to = False
        self.action_update = False
        self.is_by = False
        self.value = -1

    def check_command(self, command: str) -> bool:
        set_regex = r"\b(?P<command>metti|imposta|setta)\b.*?\bvolume\b.+?\ba\b.+?\b(?P<value>\d+)\b"

        if re.search(set_regex, command) is not None:
            self.value = retrieve_number_in_string(command)
            self.action_set = True
            self.is_to = True
            return True

        update_regex = r"\b(?P<command>alza|abbassa)\b.*?\bvolume\b.+?\b(a|di)\b.+?\b(?P<value>\d+)\b"

        if re.search(update_regex, command) is not None:
            if " di " in command:
                self.is_by = True
            else:
                self.is_to = True

            self.value = retrieve_number_in_string(command)
            self.action_update = True
            return True

        return False

    def execute(self, command: str) -> str:

        try:
            # Retrieve audio settings
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume_object = cast(interface, POINTER(IAudioEndpointVolume))

            current_volume = volume_object.GetMasterVolumeLevelScalar()

            val = self.find_new_volume(command, current_volume)

            volume_object.SetMasterVolumeLevelScalar(val, None)

        except OSError:
            print("There was a problem with the SO")

        return "Ho modificato il volume"

    # Returns a nev volume value in the range [0,1]
    def find_new_volume(self, command: str, current_volume: float) -> float:
        # "... [Setta / Alza / Imposta]/[Alza / Abbassa] ... A ..."
        if self.is_to and (self.action_set or self.action_update):
            return self.value / 100

        # "... [Alza / Abbassa] ... DI ..."
        elif self.is_by and self.action_update:
            # Current volume
            val = int(round(current_volume * 100))

            # Up or down?
            if "alza" in command:
                val = clamp_val(val + self.value) / 100
            elif "abbassa" in command:
                val = clamp_val(val - self.value) / 100

            return val

        # Should not happen
        return current_volume
