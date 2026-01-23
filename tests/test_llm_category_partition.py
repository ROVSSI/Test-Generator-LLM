import pytest
import os, importlib.util

BASE_DIR = os.path.dirname(__file__)
TARGET_PATH = os.path.join(BASE_DIR, '..', 'src', 'sample_code.py')
spec = importlib.util.spec_from_file_location('target_module', TARGET_PATH)
target_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(target_module)

def test_add_tc1():
    result = target_module.add(2, 3)
    assert result is not None

def test_add_tc2():
    result = target_module.add(2.5, 3.5)
    assert result is not None

def test_add_tc3():
    result = target_module.add(2, 3.5)
    assert result is not None

def test_add_tc4():
    result = target_module.add(-2, -3)
    assert result is not None

def test_add_tc5():
    result = target_module.add(-2.5, -3.5)
    assert result is not None
