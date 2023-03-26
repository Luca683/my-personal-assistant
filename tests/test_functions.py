import sys
import os
from typing import List
import pytest
from pytest_mock import MockerFixture

src_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))
sys.path.append(src_folder)

import src.myAssistant

from mod_volume import ModuleVolume

# We cannot test inputCommand(), beacuse the objects used in it are not defined during tests runned from a virtual environment
def test_inputCommand(mocker: MockerFixture) -> None:
    # arrange
    mock_return = "Ciao moNdo"
    mocker.patch.object(src.myAssistant.reco, "listen", return_value=mock_return)
    mocker.patch.object(src.myAssistant.reco, "recognize_google", return_value=mock_return)

    # act
    res = src.myAssistant.inputCommand()

    # assert
    assert isinstance(res, str)

    ##if(src.myAssistant.hasMicrophone is False):
    ##    assert res == "question_name_ex"
    ##else:
    ##    assert res == mock_return.lower()


def test_findModule():
    res = src.myAssistant.findModule("abbassa volume di 150")
    assert isinstance(res, ModuleVolume)

    res = src.myAssistant.findModule("Ciao mondo")
    assert res is None

functionalities_tests: List[dict] = [
    # False commands
    {"command": "stop", "check_command_res": True},
    {"command": "_NoQuestion", "check_command_res": False},
    {"command" : "metti volume a 20", "check_command_res": False},
]

@pytest.mark.parametrize("test", functionalities_tests)
def test_execute(mocker: MockerFixture, test: dict) -> None:
    # arrange
    mock_return = test["command"]
    mocker.patch.object(src.myAssistant, "inputCommand", return_value=mock_return)

    # Mock speak() or it will trigger during test
    mocker.patch.object(src.myAssistant, "speak", return_value=None)

    # act
    res = src.myAssistant.execute()

    # assert
    assert isinstance(res, bool)
    assert res is test["check_command_res"]
