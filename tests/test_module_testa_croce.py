import sys
import os
from pytest_mock import MockerFixture

src_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))
sys.path.append(src_folder)

from src.mod_testa_croce import ModuleTestaCroce
from typing import List
import pytest
import random

functionalities_tests: List[dict] = [
    #False commands
    {"command": "", "check_command_res": False},
    {"command": "test", "check_command_res": False},
    {"command": "giochiamo", "check_command_res": False},
    {"command": "moneta", "check_command_res": False},

    #True Commands
    {"command": "testa o croce", "check_command_res": True},
    {"command": "croce o testa", "check_command_res": True},
    {"command": "giochiamo a testa o croce", "check_command_res": True},
    {"command": "giochiamo a croce o testa", "check_command_res": True},
    {"command": "lancia una moneta", "check_command_res": True},
    {"command": "lancia la moneta", "check_command_res": True},
    {"command": "tira la moneta", "check_command_res": True},
    {"command": "tira una moneta", "check_command_res": True},
]

money_value: List[dict] = [
    {"value": 0, "response": "È uscito testa"},
    {"value": 1, "response": "È uscito croce"}
]

@pytest.mark.parametrize("test", functionalities_tests)
@pytest.mark.parametrize("money", money_value)
def test_functionalities(mocker: MockerFixture, test: dict, money: dict) -> None:
    testa_croce = ModuleTestaCroce()

    #Test comando
    assert testa_croce.check_command(test["command"]) == test["check_command_res"]

    if not test["check_command_res"]:
        return
    
    #Test moneta
    mocker.patch.object(random, "randint", return_value=money["value"])
    response = testa_croce.execute(test["command"])

    assert response == money["response"]
    

