import pytest
import os, importlib.util

BASE_DIR = os.path.dirname(__file__)
TARGET_PATH = os.path.join(BASE_DIR, '..', 'src', 'order_routing_code.py')
spec = importlib.util.spec_from_file_location('target_module', TARGET_PATH)
target_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(target_module)

def test_route_order_tc1():
    with pytest.raises(ValueError):
        target_module.route_order(order_total=-1, customer_tier='standard', is_express=False, has_coupon=False, destination='domestic')

def test_route_order_tc2():
    result = target_module.route_order(order_total=0, customer_tier='standard', is_express=False, has_coupon=False, destination='domestic')
    assert result == 'manual_review'

def test_route_order_tc3():
    with pytest.raises(ValueError):
        target_module.route_order(order_total=10, customer_tier='platinum', is_express=False, has_coupon=False, destination='domestic')

def test_route_order_tc4():
    result = target_module.route_order(order_total=10, customer_tier='gold', is_express=False, has_coupon=False, destination='domestic')
    assert result == 'vip_free_shipping'

def test_route_order_tc5():
    with pytest.raises(ValueError):
        target_module.route_order(order_total=10, customer_tier='standard', is_express=False, has_coupon=False, destination='space')

def test_route_order_tc6():
    result = target_module.route_order(order_total=10, customer_tier='standard', is_express=False, has_coupon=False, destination='domestic')
    assert result == 'manual_review'

def test_route_order_tc7():
    with pytest.raises(ValueError):
        target_module.route_order(order_total=30, customer_tier='standard', is_express=True, has_coupon=False, destination='international')

def test_route_order_tc8():
    result = target_module.route_order(order_total=50, customer_tier='standard', is_express=True, has_coupon=False, destination='international')
    assert result == 'international_express'

def test_route_order_tc9():
    result = target_module.route_order(order_total=150, customer_tier='gold', is_express=False, has_coupon=True, destination='domestic')
    assert result == 'vip_free_shipping_discount'

def test_route_order_tc10():
    result = target_module.route_order(order_total=150, customer_tier='gold', is_express=False, has_coupon=False, destination='domestic')
    assert result == 'vip_free_shipping'

def test_route_order_tc11():
    result = target_module.route_order(order_total=150, customer_tier='silver', is_express=False, has_coupon=False, destination='domestic')
    assert result == 'vip_free_shipping'

def test_route_order_tc12():
    result = target_module.route_order(order_total=100, customer_tier='gold', is_express=False, has_coupon=False, destination='domestic')
    assert result == 'vip_free_shipping'

def test_route_order_tc13():
    with pytest.raises(ValueError):
        target_module.route_order(order_total=30, customer_tier='standard', is_express=True, has_coupon=False, destination='international')

def test_route_order_tc14():
    result = target_module.route_order(order_total=50, customer_tier='standard', is_express=True, has_coupon=False, destination='international')
    assert result == 'international_express'

def test_route_order_tc15():
    result = target_module.route_order(order_total=70, customer_tier='standard', is_express=False, has_coupon=True, destination='domestic')
    assert result == 'standard'

def test_route_order_tc16():
    result = target_module.route_order(order_total=80, customer_tier='standard', is_express=False, has_coupon=True, destination='domestic')
    assert result == 'discount_only'

def test_route_order_tc17():
    result = target_module.route_order(order_total=10, customer_tier='standard', is_express=False, has_coupon=False, destination='domestic')
    assert result == 'manual_review'

def test_route_order_tc18():
    result = target_module.route_order(order_total=20, customer_tier='standard', is_express=False, has_coupon=False, destination='domestic')
    assert result == 'standard'
