import init, { Params } from "./js_wasm_bindgen.js";

export async function main() {
    await init();

    document.getElementById("source").innerText = example.toString();
    example(Params);
}

function example() {
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
        print("= " + params.get("hello"));
        print()
    }
    finally {
        print("Free instance")
        params.free();
    }
}

const print = function(text) {
    const output = document.getElementById("output");
    output.innerText += (text || "") + "\n";
}
