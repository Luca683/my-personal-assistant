import sys
import os
from pytest_mock import MockerFixture


src_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))
sys.path.append(src_folder)
import pyjokes
from src.mod_time import ModuleTime
from typing import List
import pytest

functionalities_tests: List[dict] = [
    # False commands
    {"command": "", "check_command_res": False},
    {"command": "test", "check_command_res": False},

    {
        "command": "che ore sono",
        "check_command_res": True,
    
    },
    {
        "command": "che ora è",
        "check_command_res": True,
    },
   
]


@pytest.mark.parametrize("test", functionalities_tests)
def test_functionalities(mocker: MockerFixture, test: dict) -> None:
    m_Time =ModuleTime()
    # Assert command check
    assert m_Time.check_command(test["command"]) == test["check_command_res"]

