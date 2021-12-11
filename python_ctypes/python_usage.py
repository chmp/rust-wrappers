import ctypes

import rust_clib


def example():
    params = Params()
    assert len(params) == 0

    params["hello"] = b"world"

    assert len(params) == 1

    print(params["hello"])


class Params:
    def __init__(self):
        self._ptr = rust_clib.params_new()

    def __del__(self):
        rust_clib.params_free(self._ptr)

    def __setitem__(self, name: str, data: bytes):
        res = rust_clib.params_insert(self._ptr, name.encode("utf8"), data, len(data))
        if res != 0:
            raise RuntimeError("Error during call to params_insert")

    def __getitem__(self, name: str) -> bytes:
        encoded_name = name.encode("utf8")
        param_len = rust_clib.params_param_len(self._ptr, encoded_name)
        param_data = rust_clib.params_param_data(self._ptr, encoded_name)

        if param_data == None or param_len < 0:
            raise KeyError(f"Could not find {name}")

        return ctypes.string_at(param_data, param_len)

    def __len__(self) -> int:
        return rust_clib.params_len(self._ptr)


if __name__ == "__main__":
    example()
