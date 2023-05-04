import sys
import os
from pytest_mock import MockerFixture

src_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))
sys.path.append(src_folder)
import pyjokes
from src.mod_jokes import ModuleJokes
from typing import List
import pytest

functionalities_tests: List[dict] = [
    # False commands
    {"command": "", "check_command_res": False},
    {"command": "test", "check_command_res": False},
    {"command": "scherzo", "check_command_res": False},

    {
        "command": "raccontami una barzelletta",
        "check_command_res": True,
        "mock_joke": "questa è una barzelletta",
        "lang": "it"
    },
    {
        "command": "raccontami una barzelletta in inglese",
        "check_command_res": True,
        "mock_joke": "i'm a joke",
        "lang": "en"
    },
    {
        "command": "dimmi una battuta in spagnolo",
        "check_command_res": True,
        "mock_joke": "soy un chiste",
        "lang": "es"
    },
    {
        "command": "dimmi una battuta in tedesco",
        "check_command_res": True,
        "mock_joke": "ich bin ein Spiel",
        "lang": "de"
    }
]


@pytest.mark.parametrize("test", functionalities_tests)
def test_functionalities(mocker: MockerFixture, test: dict) -> None:
    m_jokes = ModuleJokes()
    # Assert command check
    assert m_jokes.check_command(test["command"]) == test["check_command_res"]

    # On False commands we don't want to assert further
    if not test["check_command_res"]:
        return

    assert m_jokes.lang == test["lang"]

    mock_val = test["mock_joke"]
    mocker.patch.object(pyjokes, "get_joke", return_value=mock_val)

    response = m_jokes.execute(test["command"])

    assert response == mock_val
