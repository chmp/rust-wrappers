# Demo code for different ways of wrapping Rust code

Directories:

- [`/rust_core`](rust_core): the wrapped rust library
- [`/rust_clib`](rust_clib): a common C library used from Python, Java and
  JavaScript
- [`/python_pyo3`](pyo3): example of using [PyO3][pyo3] to wrap the rust library
  for Python
- [`/python_cffi`](python_cffi): wrap the [common C library](rust_clib) using
  [CFFI][cffi]
- [`/python_ctypes`](python_ctypes): wrap the [common C library](rust_clib)
  using [ctypes][ctypes]
- [`/python_wasm`](python_wasm): Python wrapper using the
  [`wasmer`][wasmer-python] Python module
- [`/java_jna`](java_jna): Java wrapper using [`jna`](jna)
- [`/java_wasm`](java_wasm): Java wrapper using the [`wasmer`](wasmer-java) Java
  library
- [`/js_wasm`](js_wasm): JavaScript wrapper running inside the browser using the
  browser [WebAssembly API][browser-wasm]

[cffi]: https://cffi.readthedocs.io/en/latest/
[ctypes]: https://docs.python.org/3/library/ctypes.html
[pyo3]: https://pyo3.rs
[wasmer-python]: https://github.com/wasmerio/wasmer-python
[wasmer-java]: https://github.com/wasmerio/wasmer-java
[jna]: https://github.com/java-native-access/jna
[browser-wasm]: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/WebAssembly

