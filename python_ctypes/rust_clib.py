from ctypes import CDLL, c_int64, c_uint64, c_void_p, c_uint8, c_char_p, string_at
from pathlib import Path

lib = CDLL(str(Path(__file__).parent.joinpath("_rust_clib.so").resolve()))

params_new = lib.params_new
params_new.argtypes = []
params_new.restype = c_void_p

params_free = lib.params_free
params_free.argtypes = [c_void_p]
params_free.restype = None

params_insert = lib.params_insert
params_insert.argtypes = [c_void_p, c_char_p, c_char_p, c_uint64]
params_insert.restype = c_uint8

params_len = lib.params_len
params_len.argtypes = [c_void_p]
params_len.restype = c_uint64

params_param_len = lib.params_param_len
params_param_len.argtypes = [c_void_p, c_char_p]
params_param_len.restype = c_int64

params_param_data = lib.params_param_data
params_param_data.argtypes = [c_void_p, c_char_p]
params_param_data.restype = c_void_p


class Params:
    def __init__(self):
        self._ptr = params_new()

    def __del__(self):
        params_free(self._ptr)

    def __setitem__(self, name: str, data: bytes):
        res = params_insert(self._ptr, name.encode("utf8"), data, len(data))
        if res != 0:
            raise RuntimeError("Error during call to params_insert")

    def __getitem__(self, name: str) -> bytes:
        encoded_name = name.encode("utf8")
        param_len = params_param_len(self._ptr, encoded_name)
        param_data = params_param_data(self._ptr, encoded_name)

        if param_data == None or param_len < 0:
            raise KeyError(f"Could not find {name}")

        return string_at(param_data, param_len)

    def __len__(self) -> int:
        return params_len(self._ptr)
