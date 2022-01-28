# `java_wasm` - using the C-ABI wrapper in Java using WebAssembly with Wasmer

This example uses the [wasmer-java](https://github.com/wasmerio/wasmer-java)
library to load Rust core compiled to WebAssembly. It requires the jar to be
installed into a local repository and the WebAssembly file to be copied into the
[resource directory](src/main/resources).

The wrapper is found in [`Params.java`](src/main/java/rust_wasm/Params.java). It
uses the low-level Wrapper found in
[`WasmRuntime.java`](src/main/java/rust_wasm/WasmRuntime.java). The use of the
`Params` class is demonstrated in the
[test](src/test/java/rust_wasm/ParamsTest.java).

To execute this example, navigate to the project root and run

```bash
python make.py java_wasm
```
