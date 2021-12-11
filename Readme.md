# Demo code for different ways of wrapping Rust code

Directories:

- [`/rust_core`](rust_core): the wrapped rust library
- [`/python_pyo3`](pyo3): example of using [PyO3][pyo3] to wrap the rust library
  for Python
- [`/common_clib`](common_clib): a common C library used from Python via ctypes,
  Java via JNA and WebAssembly

[pyo3]: https://pyo3.rs
