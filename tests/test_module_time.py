import sys
import os
from pytest_mock import MockerFixture
import datetime

src_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))
sys.path.append(src_folder)
from src.mod_time import ModuleTime
from typing import List
import pytest
from src.mod_time import convert_month
from src.mod_time import convert_week_day

functionalities_tests: List[dict] = [
    # False commands
    {"command": "", "check_command_res": False},
    {"command": "test", "check_command_res": False},

    {
     "command": "che ore sono","check_command_res": True,
     "time":True,"day":False,"date":False, "expected_result":"Sono le: 15:30 "
    },  
    {
     "command": "che ora Ã¨","check_command_res": True,
     "time":True,"day":False,"date":False, "expected_result":"Sono le: 15:30 "
    },
    {
      "command":"dimmi l'ora e il giorno","check_command_res":True,
      "time":True,"day":True,"date":False, "expected_result":"Sono le: 15:30 Oggi Ã¨: MartedÃ¬ "  
    },
    { 
    "command":"dimmi che giorno Ã¨ oggi ","check_command_res":True,
    "time":False,"day":True,"date":False, "expected_result":"Oggi Ã¨: MartedÃ¬ " 
    },
    {
     "command":"dimmi la data di oggi","check_command_res":True,
     "time":False,"day":False,"date":True, "expected_result":"Data: 16/Maggio/2023 "  
    }
   
]


@pytest.mark.parametrize("test", functionalities_tests)
def test_functionalities(mocker: MockerFixture, test: dict) -> None:
    m_time = ModuleTime()
    # Assert command check
    assert m_time.check_command(test["command"]) == test["check_command_res"]
    # On False commands we don't want to assert further
    if not test["check_command_res"]:
        return
    
    #mock_now = datetime.datetime(2023, 5, 16, 15, 30, 45, 123456)
    #mocker.patch.object(datetime.datetime, "now", return_value=mock_now)
    mock_now = datetime.datetime(2023, 5, 16, 15, 30, 45, 123456)
    mocker.patch.object(datetime, 'datetime', mocker.Mock(wraps=datetime.datetime, now=mocker.Mock(return_value=mock_now)))
    
    response = m_time.execute(test["command"])

    assert response == test["expected_result"]


month_tests: List[dict] = [
    {"input": 1, "expected_output": "Gennaio"},
    {"input": 5, "expected_output": "Maggio"},
    {"input": 12, "expected_output": "Dicembre"},
]

@pytest.mark.parametrize("test", month_tests)
def test_convert_month(test: dict) -> None:
    result = convert_month(test["input"])

    assert result == test["expected_output"]
    
week_day_tests: List[dict] = [
    {"input": "Monday", "expected_output": "LunedÃ¬"},
    {"input": "Saturday", "expected_output": "Sabato"},
    {"input": "Sunday", "expected_output": "Domenica"},
]

@pytest.mark.parametrize("test", week_day_tests)
def test_convert_week_day(test: dict) -> None:
    result = convert_week_day(test["input"])

    assert result == test["expected_output"]