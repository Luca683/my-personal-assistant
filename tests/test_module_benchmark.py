import sys
import psutil
import os

src_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))
sys.path.append(src_folder)

from typing import List
import pytest
from pytest_mock import MockerFixture
from src.mod_benchmark import ModuleBenchmark


functionalities_tests: List[dict] = [
    {"command": "", "check_command_res": False},
    {"command": "dammi i benchmark", "check_command_res": False},
    {"command": "sistema e processore", "check_command_res": False},
    {"command": "dammi i benchmark del sistema", "check_command_res": True, 
     "hasCpu": True, "hasRam": True, "hasBattery": True,
     "result": "La percentuale di utilizzo della CPU è del 3.3 percento, "
     + "la percentuale di utilizzo della RAM è del 55.4 percento, "
     + "che ammonta a 3.51 gigabyte utilizzati, la batteria è al 13.0 percento, e non è alimentata"},
    {"command": "dimmi i benchmark della processore", "check_command_res": True,
     "hasCpu": True, "hasRam": False, "hasBattery": False,
     "result": "La percentuale di utilizzo della CPU è del 3.3 percento, "},
    {"command": "dammi le prestazioni della ram", "check_command_res": True, 
     "hasCpu": False, "hasRam": True, "hasBattery": False,
     "result": "la percentuale di utilizzo della RAM è del 55.4 percento, "
     + "che ammonta a 3.51 gigabyte utilizzati, "},
    {"command": "dammi le prestazioni della ram e della batteria", "check_command_res": True, 
     "hasCpu": False, "hasRam": True, "hasBattery": True,
     "result": "la percentuale di utilizzo della RAM è del 55.4 percento, "
     + "che ammonta a 3.51 gigabyte utilizzati, la batteria è al 13.0 percento, e non è alimentata"}
]


@pytest.mark.parametrize("test", functionalities_tests)
def test_functionalities(mocker: MockerFixture, test: dict) -> None:
    m_benchmark = ModuleBenchmark()

    # Assert command check
    assert m_benchmark.check_command(test["command"]) == test["check_command_res"]

    # On False commands we don't want to assert further
    if not test["check_command_res"]:
        return
    
    assert m_benchmark.benchmark_ram == test["hasRam"]
    assert m_benchmark.benchmark_cpu == test["hasCpu"]
    assert m_benchmark.benchmark_battery == test["hasBattery"]

    # arrange
    mock_cpu = 3.3
    mock_virtualMem = [0, 0, 55.4, 3.512345]
    mock_battery = [13.0, 0, False]
    mocker.patch.object(psutil, "cpu_percent", return_value=mock_cpu)
    mocker.patch.object(psutil, "virtual_memory", return_value=mock_virtualMem)
    mocker.patch.object(psutil, "sensors_battery", return_value=mock_battery)

    res = m_benchmark.execute(test["command"])

    assert res == test["result"]


format_tests: List[dict] = [
    {"val": "12.3456", "expected": "12.34"},
    {"val": "1.23456", "expected": "1.23"}
]

@pytest.mark.parametrize("test", format_tests)
def test_formatPercentage(test: dict) -> None:
    m_benchmark = ModuleBenchmark()

    res = m_benchmark.formatPercentage(test["val"])

    assert res == test["expected"]