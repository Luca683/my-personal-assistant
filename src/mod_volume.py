from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

action_set = False
is_to = False
action_up_down = False
is_by = False


def check_command(command) -> bool:
    if "volume" not in command:
        return False

    global action_set
    global is_to
    global action_up_down
    global is_by

    action_set = ("setta" in command or "imposta" in command or "metti" in command)
    print(action_set)

    is_to = "a" in command
    print(is_to)

    # "Setta il volume A x" non avrebbe senso altrimenti
    if action_set and not is_to:
        return False

    action_up_down = ("alza" in command or "abbassa" in command)
    print(action_up_down)

    is_by = "di" in command
    print(is_by)

    # Manca il verbo
    if not action_up_down and not action_set:
        return False

    # "Setta di x il volume" non ha senso
    if action_set and is_by:
        return False

    # "Alza di" o "Alza a" altrimenti non vrebbe senso
    if action_up_down and (not is_to and not is_by):
        return False

    return True


def execute(command) -> str | bool:
    words = command.split(" ")

    global action_set
    global is_to
    global action_up_down
    global is_by

    try:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))

        if action_set and is_to:
            # [0, 100] in [-65, 0]: val - 100 * 1,538
            # x =
            volume.SetMasterVolumeLevel(-15.0, None)

    except OSError:
        print("There was a problem with the SO")

    return "Ho modificato il volume"
