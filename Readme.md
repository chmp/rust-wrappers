# Demo code for different ways of wrapping Rust code

This repository showcases different ways of wrapping Rust code in different
language (Python, Java, JavaScript). The running example is an object storing
parameters as byte arrays (see [here](rust_core/src/lib.rs) for more details).

The different examples can be executed with the `make.py` script. Currently the
 code assumes a Linux system. To run all execute:

```bash
python make.py all
```

To run the Java examples, first the [Wasmer][wasmer-java] jar needs to be
installed into the local repository. To do so,

1. Fetch the 0.3.0 jar from the release page in the [wasmer-java][wasmer-java]
   repository
2. Run

    ```python
    python make.py install-wasmer-jar {PATH_TO_JAR}
    ```

To generate the `js_wasm_bindgen` example, the [`wasm-bindgen`][wasm-bindgen]
CLI needs to be installed. To so run:

```bash
cargo install wasm-bindgen-cli
```

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
- [`/js_wasm_bindgen`](js_wasm_bindgen): JavaScript wrapper running inside the
  browser using [wasm-bindgen][wasm-bindgen] to generate the glue code

[cffi]: https://cffi.readthedocs.io/en/latest/
[ctypes]: https://docs.python.org/3/library/ctypes.html
[pyo3]: https://pyo3.rs
[wasmer-python]: https://github.com/wasmerio/wasmer-python
[wasmer-java]: https://github.com/wasmerio/wasmer-java
[jna]: https://github.com/java-native-access/jna
[browser-wasm]: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/WebAssembly
[wasm-bindgen]: https://github.com/rustwasm/wasm-bindgen
