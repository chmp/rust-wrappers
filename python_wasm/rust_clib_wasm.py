from pathlib import Path

from wasmer import Store, Module, Instance

with open(Path(__file__).parent.joinpath("rust_clib.wasm"), "rb") as fobj:
    instance = Instance(Module(Store(), fobj.read()))


memory = instance.exports.memory
allocate = instance.exports.allocate

params_new = instance.exports.params_new
params_free = instance.exports.params_free
params_insert = instance.exports.params_insert
params_len = instance.exports.params_len
params_param_len = instance.exports.params_param_len
params_param_data = instance.exports.params_param_data


class Params:
    def __init__(self):
        self._ptr = params_new()

    def __del__(self):
        params_free(self._ptr)

    def __setitem__(self, name: str, data: bytes):
        name_ptr, data_ptr = _store_setitem_args(name, data)

        res = params_insert(self._ptr, name_ptr, data_ptr, len(data))
        if res != 0:
            raise RuntimeError("Error during call to params_insert")

    def __getitem__(self, name: str) -> bytes:
        name_ptr = _store_getitem_args(name)
        param_len = params_param_len(self._ptr, name_ptr)
        param_data = params_param_data(self._ptr, name_ptr)

        if param_data == None or param_len < 0:
            raise KeyError(f"Could not find {name}")

        return _load_getitem_result(param_data, param_len)

    def __len__(self) -> int:
        return params_len(self._ptr)


def _store_setitem_args(name, data):
    encoded_name = name.encode("utf8")

    buf_ptr = allocate(len(encoded_name) + 1 + len(data))

    name_start = buf_ptr
    name_end = buf_ptr + len(encoded_name)
    data_start = buf_ptr + len(encoded_name) + 1
    data_end = buf_ptr + len(encoded_name) + 1 + len(data)

    # NOTE: on master using memory.buffer would be much faster
    # the relevant code changes are not released yet as a stable package
    view = memory.uint8_view()
    view[name_start:name_end] = encoded_name
    view[name_end] = 0
    view[data_start:data_end] = data

    return name_start, data_start


def _store_getitem_args(name):
    encoded_name = name.encode("utf8")

    buf_ptr = allocate(len(encoded_name) + 1)

    name_start = buf_ptr
    name_end = buf_ptr + len(encoded_name)

    view = memory.uint8_view()
    view[name_start:name_end] = encoded_name
    view[name_end] = 0

    return name_start


def _load_getitem_result(param_data, param_len):
    view = memory.uint8_view()
    return bytes(view[param_data : param_data + param_len])
