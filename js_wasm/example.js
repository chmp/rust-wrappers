(function() {
"use strict";

window.main = async function() {
    const instance = await loadWasmLib();
    const Params = defineParamsClass(instance);

    document.getElementById("source").innerText = example.toString();
    example(Params);
}

const example = function example(Params) {
    print("Define new params instance");
    const params = new Params();

    try {
        print("ptr " + params.ptr);
        print("len " + params.len());
        print()

        print("Set item 'hello'")
        params.set("hello", [0, 1, 2, 3]);
        print("len " + params.len());
        print()

        print("Get item 'hello'");
        print("= " + JSON.stringify(params.get("hello")));
        print()
    }
    catch(err) {
        console.error(err)
        print("Error: " + err)
        print()
    }
    finally {
        print("Free instance")
        params.free();
    }
}

const loadWasmLib = async function() {
    const imports = {};
    const res = await WebAssembly.instantiateStreaming(
        fetch('rust_clib.wasm'),
        imports,
    );

    return res.instance;
}

const print = function(text) {
    const output = document.getElementById("output");
    output.innerText += (text || "") + "\n";
}
})();