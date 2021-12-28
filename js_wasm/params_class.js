(function() {
"use strict";

window.defineParamsClass = instance => {
    const textEncoder = new TextEncoder();

    function Params() {
        this.ptr = instance.exports.params_new();
    }

    Params.prototype.free = function free() {
        if(this.ptr != null) {
            instance.exports.params_free(this.ptr);
        }
        this.ptr = null;
    }

    Params.prototype.len = function len() {
        return Number(instance.exports.params_len(this.ptr));
    }

    Params.prototype.set = function set(key, value) {
        const [namePtr, dataPtr] = storeSetArgs(key, value);

        const res = instance.exports.params_insert(this.ptr, namePtr, dataPtr, BigInt(value.length));
        if(res != 0) {
            throw new Error("Error during call to params_insert")
        }

    }

    Params.prototype.get = function get(key) {
        const keyPtr = storeGetArgs(key);

        const paramLen = instance.exports.params_param_len(this.ptr, keyPtr)
        const paramPtr = instance.exports.params_param_data(this.ptr, keyPtr)

        if((paramPtr == 0) || (paramLen < 0)) {
            throw Error("Could not get " + key);
        }

        return loadGetResult(paramPtr, paramLen);
    }

    const storeSetArgs = function(key, value) {
        const encodedKey = textEncoder.encode(key);
        const bufPtr = instance.exports.allocate(BigInt(encodedKey.length + 1 + value.length));
        const memory = new Uint8Array(instance.exports.memory.buffer);

        for(var i = 0; i < encodedKey.length; i++) {
            memory[bufPtr + i] = encodedKey[i];
        }
        memory[bufPtr + encodedKey.length] = 0;
        for(var i = 0; i < value.length; i++) {
            memory[bufPtr + encodedKey.length + 1 + i] = value[i];
        }

        return [bufPtr, bufPtr + encodedKey.length + 1];
    }

    const storeGetArgs = function(key) {
        const encodedKey = textEncoder.encode(key);
        const bufPtr = instance.exports.allocate(BigInt(encodedKey.length + 1));
        const memory = new Uint8Array(instance.exports.memory.buffer);

        for(var i = 0; i < encodedKey.length; i++) {
            memory[bufPtr + i] = encodedKey[i];
        }
        memory[bufPtr + encodedKey.length] = 0;

        return bufPtr;
    }

    const loadGetResult = function(ptr, len) {
        const memory = new Uint8Array(instance.exports.memory.buffer);
        const res = [];

        for(var i = 0; i < len; i++) {
            res.push(memory[ptr + i]);
        }

        return res;
    }

    return Params;
}

})()