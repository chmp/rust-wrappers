# `js_wasm_bindgen` - JavaScript example using `wasm-bindgen` 

The example has to run in a local web server, as it dynamically loads the
WebAssembly module. You can  start for example via:

```bash
cd example
python -m http.server
```

Afterwards, the example can be access at "http://localhost:8080". 

To build the  this WebAssembly module, navigate to the project root and run

```bash
python make.py js_wasm_bindgen
```
