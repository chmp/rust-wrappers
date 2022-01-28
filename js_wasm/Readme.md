# `js_wasm` - JavaScript example using WebAssembly

Files:

- [`params_class.js`](params_class.js): the wrapper around the WebAssembly module. It defines a
  function `defineParamsClass` that takes the WebAssembly instance as its
  argument and that returns the wrapper class. 
- [`example.js`](example.js): the example script that demonstrate how to use the
  generated wrapper
- [`index.html`](index.html): the HTML file tying everything together

The example has to be run in a local web server, as it dynamically loads the
WebAssembly module. You can  start for example via `python -m http.server`.
Afterwards, the example can be access at "http://localhost:8080". 

To build the  this WebAssembly module, navigate to the project root and run

```bash
python make.py js_wasm
```
