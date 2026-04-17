import pytest
import os, importlib.util

BASE_DIR = os.path.dirname(__file__)
TARGET_PATH = os.path.join(BASE_DIR, '..', 'src', 'refund_policy_code.py')
spec = importlib.util.spec_from_file_location('target_module', TARGET_PATH)
target_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(target_module)

def test_assess_refund_request_tc1():
    result = target_module.assess_refund_request(order_total=100, days_since_purchase=10, customer_tier='standard', item_condition='unopened', has_receipt=True, payment_risk_flag=False)
    assert result == 'full_refund'

def test_assess_refund_request_tc2():
    result = target_module.assess_refund_request(order_total=50, days_since_purchase=20, customer_tier='silver', item_condition='damaged', has_receipt=True, payment_risk_flag=False)
    assert result == 'replacement'

def test_assess_refund_request_tc3():
    result = target_module.assess_refund_request(order_total=150, days_since_purchase=5, customer_tier='silver', item_condition='opened', has_receipt=True, payment_risk_flag=True)
    assert result == 'manual_investigation'

def test_assess_refund_request_tc4():
    result = target_module.assess_refund_request(order_total=50, days_since_purchase=61, customer_tier='standard', item_condition='unopened', has_receipt=True, payment_risk_flag=False)
    assert result == 'rejected_window'

def test_assess_refund_request_tc5():
    result = target_module.assess_refund_request(order_total=200, days_since_purchase=10, customer_tier='standard', item_condition='opened', has_receipt=False, payment_risk_flag=False)
    assert result == 'manual_review'

def test_assess_refund_request_tc6():
    result = target_module.assess_refund_request(order_total=75, days_since_purchase=10, customer_tier='gold', item_condition='opened', has_receipt=True, payment_risk_flag=False)
    assert result == 'store_credit'

def test_assess_refund_request_tc7():
    result = target_module.assess_refund_request(order_total=50, days_since_purchase=20, customer_tier='gold', item_condition='opened', has_receipt=True, payment_risk_flag=False)
    assert result == 'store_credit'

def test_assess_refund_request_tc8():
    result = target_module.assess_refund_request(order_total=50, days_since_purchase=40, customer_tier='silver', item_condition='damaged', has_receipt=True, payment_risk_flag=False)
    assert result == 'rejected_policy'

def test_assess_refund_request_tc9():
    with pytest.raises(ValueError):
        target_module.assess_refund_request(order_total=-1, days_since_purchase=0, customer_tier='standard', item_condition='unopened', has_receipt=True, payment_risk_flag=False)

def test_assess_refund_request_tc10():
    with pytest.raises(ValueError):
        target_module.assess_refund_request(order_total=0, days_since_purchase=-1, customer_tier='standard', item_condition='unopened', has_receipt=True, payment_risk_flag=False)

def test_assess_refund_request_tc11():
    with pytest.raises(ValueError):
        target_module.assess_refund_request(order_total=0, days_since_purchase=0, customer_tier='invalid_tier', item_condition='unopened', has_receipt=True, payment_risk_flag=False)

def test_assess_refund_request_tc12():
    with pytest.raises(ValueError):
        target_module.assess_refund_request(order_total=0, days_since_purchase=0, customer_tier='standard', item_condition='invalid_condition', has_receipt=True, payment_risk_flag=False)
