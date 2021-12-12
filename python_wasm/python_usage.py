import pytest
from rust_clib_wasm import Params


params = Params()
assert len(params) == 0

params["hello"] = b"world"
assert len(params) == 1
assert params["hello"] == b"world"

with pytest.raises(KeyError):
    params["missing"]
