import pytest
import os, importlib.util

BASE_DIR = os.path.dirname(__file__)
TARGET_PATH = os.path.join(BASE_DIR, '..', 'src', 'complex_code.py')
spec = importlib.util.spec_from_file_location('target_module', TARGET_PATH)
target_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(target_module)

def test_authorize_tc1():
    result = target_module.authorize(user_role='admin', is_active=True, has_2fa=True)
    assert result is True

def test_authorize_tc2():
    result = target_module.authorize(user_role='user', is_active=True, has_2fa=True)
    assert result is True

def test_authorize_tc3():
    result = target_module.authorize(user_role='user', is_active=True, has_2fa=False)
    assert result is False

def test_authorize_tc4():
    result = target_module.authorize(user_role='user', is_active=False, has_2fa=True)
    assert result is False

def test_authorize_tc5():
    result = target_module.authorize(user_role='user', is_active=False, has_2fa=False)
    assert result is False
