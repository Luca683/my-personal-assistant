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
    # print(action_set)

    is_to = " a " in command
    # print(is_to)

    # "Setta il volume A x" non avrebbe senso altrimenti
    if action_set and not is_to:
        return False

    action_up_down = ("alza" in command or "abbassa" in command)
    # print(action_up_down)

    is_by = " di " in command
    # print(is_by)

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
    # words = command.split(" ")

    global action_set
    global is_to
    global action_up_down
    global is_by

    number = ""

    # Retrieve number value in the command
    flag = 0
    for w in command:
        if w.isdigit():
            number += w
            flag = 1
        elif flag == 1:
            break

    # There is no number in the command
    if number == "":
        print("Perfavore specifica anche un valore numerico")
        return "Perfavore specifica anche un valore numerico"

    number = clamp_val(int(number))

    try:
        # Retrieve audio settings
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))

        # "... [Setta / Alza / Abbassa] ... A ..."
        if is_to and (action_set or action_up_down):
            # print("Setto a...")

            number = number / 100
            volume.SetMasterVolumeLevelScalar(number, None)

        # "... [Alza / Abbassa] ... DI ..."
        elif is_by and action_up_down:
            # print("Modifico di...")

            # Current volume
            current_vol = int(round(volume.GetMasterVolumeLevelScalar() * 100))

            # Up or down?
            up = "alza" in command

            if up:
                x = clamp_val(current_vol + number) / 100
                volume.SetMasterVolumeLevelScalar(x, None)
            else:
                down = "abbassa" in command

                if down:
                    x = clamp_val(current_vol - number) / 100
                    volume.SetMasterVolumeLevelScalar(x, None)

        # ...

    except OSError:
        print("There was a problem with the SO")

    return "Ho modificato il volume"


# Clamp values between 0 and 100
def clamp_val(number) -> int:
    if number < 0:
        return 0
    elif number > 100:
        return 100

    return number
