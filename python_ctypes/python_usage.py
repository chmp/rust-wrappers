import rust_clib


def example():
    params = Params()
    assert len(params) == 0

    params["hello"] = b"world"

    assert len(params) == 1


class Params:
    def __init__(self):
        self._ptr = rust_clib.params_new()

    def __del__(self):
        rust_clib.params_free(self._ptr)

    def __setitem__(self, name: str, data: bytes):
        res = rust_clib.params_insert(self._ptr, name.encode("utf8"), data, len(data))
        if res != 0:
            raise RuntimeError("Error during call to params_insert")

    def __len__(self):
        return rust_clib.params_len(self._ptr)


if __name__ == "__main__":
    example()
