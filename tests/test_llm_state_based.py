import pytest
import os, importlib.util

BASE_DIR = os.path.dirname(__file__)
TARGET_PATH = os.path.join(BASE_DIR, '..', 'src', 'refund_case_code.py')
spec = importlib.util.spec_from_file_location('target_module', TARGET_PATH)
target_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(target_module)

def test_refundcase_tc1():
    obj = target_module.RefundCase()
    assert obj.state == 'draft'
    result = obj.submit()
    assert result == 'submitted'
    assert obj.state == 'submitted'

def test_refundcase_tc2():
    obj = target_module.RefundCase()
    assert obj.state == 'draft'
    result = obj.submit()
    assert result == 'submitted'
    assert obj.state == 'submitted'
    result = obj.submit()
    assert result == 'already_submitted'
    assert obj.state == 'submitted'

def test_refundcase_tc3():
    obj = target_module.RefundCase()
    assert obj.state == 'draft'
    with pytest.raises(ValueError):
        obj.flag_for_review()
    assert obj.state == 'draft'

def test_refundcase_tc4():
    obj = target_module.RefundCase()
    assert obj.state == 'draft'
    result = obj.submit()
    assert result == 'submitted'
    assert obj.state == 'submitted'
    result = obj.flag_for_review()
    assert result == 'under_review'
    assert obj.state == 'under_review'

def test_refundcase_tc5():
    obj = target_module.RefundCase()
    assert obj.state == 'draft'
    result = obj.submit()
    assert result == 'submitted'
    assert obj.state == 'submitted'
    result = obj.approve(refund_amount=100)
    assert result == 'approved'
    assert obj.state == 'approved'

def test_refundcase_tc6():
    obj = target_module.RefundCase()
    assert obj.state == 'draft'
    result = obj.submit()
    assert result == 'submitted'
    assert obj.state == 'submitted'
    result = obj.reject(reason='not valid')
    assert result == 'rejected'
    assert obj.state == 'rejected'

def test_refundcase_tc7():
    obj = target_module.RefundCase()
    assert obj.state == 'draft'
    result = obj.submit()
    assert result == 'submitted'
    assert obj.state == 'submitted'
    result = obj.approve(refund_amount=100)
    assert result == 'approved'
    assert obj.state == 'approved'
    result = obj.close()
    assert result == 'closed'
    assert obj.state == 'closed'

def test_refundcase_tc8():
    obj = target_module.RefundCase()
    assert obj.state == 'draft'
    result = obj.submit()
    assert result == 'submitted'
    assert obj.state == 'submitted'
    result = obj.reject(reason='not valid')
    assert result == 'rejected'
    assert obj.state == 'rejected'
    result = obj.close()
    assert result == 'closed'
    assert obj.state == 'closed'
