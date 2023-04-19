import sys
import os

src_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))
sys.path.append(src_folder)

from typing import List
import pytest
from src.mod_benchmark import ModuleBenchmark


functionalities_tests: List[dict] = [
    # False commands
    {"command": "", "check_command_res": False},
    {"command": "dammi i benchmark", "check_command_res": False},
    {"command": "sistema e cpu", "check_command_res": False},
    {"command": "dammi i benchmark del sistema", "check_command_res": True, "isCpu": True, "isRam": True},
    {"command": "dimmi i benchmark della cpu", "check_command_res": True, "isCpu": True, "isRam": False},
    {"command": "dammi le prestazioni della ram", "check_command_res": True, "isCpu": False, "isRam": True}
]


@pytest.mark.parametrize("test", functionalities_tests)
def test_functionalities(test: dict) -> None:
    m_bench = ModuleBenchmark()

    # Assert command check
    assert m_bench.check_command(test["command"]) == test["check_command_res"]

    # On False commands we don't want to assert further
    if not test["check_command_res"]:
        return
    
    assert m_bench.benchmark_ram == test["isRam"]
    assert m_bench.benchmark_cpu == test["isCpu"]
