from ctypes import CDLL, c_int64, c_uint64, c_void_p, c_uint8, c_char_p
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
