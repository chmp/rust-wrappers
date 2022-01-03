from cffi import FFI

ffi = FFI()
ffi.cdef(
    """
    void* params_new();
    void params_free(void*);
    uint8_t params_insert(void*, char*, char*, uint64_t);
    uint64_t params_len(void*);
    int64_t params_param_len(void*, char*);
    void* params_param_data(void*, char*);
"""
)

lib = ffi.dlopen("./_rust_clib.so")


class Params:
    def __init__(self):
        self._ptr = lib.params_new()

    def __del__(self):
        lib.params_free(self._ptr)

    def __setitem__(self, name: str, data: bytes):
        with ffi.from_buffer(data) as data:
            res = lib.params_insert(self._ptr, name.encode("utf8"), data, len(data))

        if res != 0:
            raise RuntimeError("Error during call to params_insert")

    def __getitem__(self, name: str) -> bytes:
        encoded_name = name.encode("utf8")
        param_len = lib.params_param_len(self._ptr, encoded_name)
        param_data = lib.params_param_data(self._ptr, encoded_name)

        if param_data == None or param_len < 0:
            raise KeyError(f"Could not find {name}")

        return ffi.buffer(param_data, param_len)

    def __len__(self) -> int:
        return lib.params_len(self._ptr)
