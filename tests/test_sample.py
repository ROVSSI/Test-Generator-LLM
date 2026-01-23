import sys, os
# Ensure src is on the path when running directly
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from sample_code import add

def test_add():
    assert add(1, 2) == 3