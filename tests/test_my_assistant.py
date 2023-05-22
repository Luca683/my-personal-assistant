import sys
import os
from typing import List
import pytest
from pytest_mock import MockerFixture

src_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))
sys.path.append(src_folder)

import src.my_assistant

from mod_volume import ModuleVolume

# We cannot test inputCommand(), beacuse the objects used in it are not defined during tests runned from a virtual environment
def test_input_command(mocker: MockerFixture) -> None:
    # arrange
    mock_return = "Ciao moNdo"
    mocker.patch.object(src.my_assistant.reco, "listen", return_value=mock_return)
    mocker.patch.object(src.my_assistant.reco, "recognize_google", return_value=mock_return)

    # act
    res = src.my_assistant.input_command()

    # assert
    assert isinstance(res, str)

def test_find_module():
    res = src.my_assistant.find_module("abbassa volume di 150")
    assert isinstance(res, ModuleVolume)

    res = src.my_assistant.find_module("Ciao mondo")
    assert res is None

functionalities_tests: List[dict] = [
    # False commands
    {"command": "stop", "check_command_res": True},
    {"command": "_NoQuestion", "check_command_res": False},
    {"command" : "metti volume a 20", "check_command_res": False},
    {"command": "alza il volume di 10", "check_command_res": False},
    {"command": "raccontami una barzelletta", "check_command_res": False},
    {"command": "dammi le prestazioni della batteria", "check_command_res": False}
]

@pytest.mark.parametrize("test", functionalities_tests)
def test_execute_command(mocker: MockerFixture, test: dict) -> None:
    # arrange
    mock_return = test["command"]
    mocker.patch.object(src.my_assistant, "input_command", return_value=mock_return)

    # Mock speak() or it will trigger during test
    mocker.patch.object(src.my_assistant, "speak", return_value=None)

    # act
    res = src.my_assistant.execute_command()

    # assert
    assert isinstance(res, bool)
    assert res is test["check_command_res"]
