import pytest
from rust_clib import Params


params = Params()
assert len(params) == 0

params["hello"] = b"w\0rld"
assert len(params) == 1
assert params["hello"] == b"w\0rld"

with pytest.raises(KeyError):
    params["missing"]
