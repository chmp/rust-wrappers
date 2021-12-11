import pytest

from pyo3_wrapper import Params

p = Params()
assert len(p) == 0

p["hello"] = b"world"
assert len(p) == 1
assert p["hello"] == b"world"

with pytest.raises(KeyError):
    p["missing"]
