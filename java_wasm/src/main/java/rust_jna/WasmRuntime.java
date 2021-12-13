package rust_jna;

import java.io.IOException;
import java.io.UnsupportedEncodingException;
import java.nio.file.Files;
import java.nio.file.Paths;

import javax.management.RuntimeErrorException;

import org.wasmer.Memory;
import org.wasmer.Instance;
import org.wasmer.exports.Function;

public class WasmRuntime {
    static WasmRuntime INSTANCE = null;

    public final Instance instance;

    public final Memory memory;

    public final Function funcAllocate;
    public final Function funcParamsNew;
    public final Function funcParamsFree;
    public final Function funcParamsInsert;
    public final Function funcParamsLen;
    public final Function funcParamsParamLen;
    public final Function funcParamsParamData;

    public synchronized static WasmRuntime get() {
        if (INSTANCE == null) {
            INSTANCE = load();
        }

        return INSTANCE;
    }

    static WasmRuntime load() {
        try {
            var wasmPath = Paths.get(WasmRuntime.class.getClassLoader().getResource("rust_clib.wasm").getPath());
            var wasmBytes = Files.readAllBytes(wasmPath);
            var instance = new Instance(wasmBytes);

            return new WasmRuntime(instance);
        } catch (IOException exc) {
            throw new RuntimeException(exc);
        }
    }

    WasmRuntime(Instance instance) {
        this.instance = instance;

        memory = instance.exports.getMemory("memory");

        funcAllocate = instance.exports.getFunction("allocate");
        funcParamsNew = instance.exports.getFunction("params_new");
        funcParamsFree = instance.exports.getFunction("params_free");
        funcParamsInsert = instance.exports.getFunction("params_insert");
        funcParamsLen = instance.exports.getFunction("params_len");
        funcParamsParamLen = instance.exports.getFunction("params_param_len");
        funcParamsParamData = instance.exports.getFunction("params_param_data");
    }

    public int allocate(long size) {
        Object[] results = funcAllocate.apply(size);
        return (Integer) results[0];
    }

    public int paramsNew() {
        Object[] results = funcParamsNew.apply();
        return (Integer) results[0];
    }

    public void paramsFree(int ptr) {
        funcParamsFree.apply(ptr);
    }

    public void paramsInsert(int ptr, String name, byte[] data) {
        var args = storeInsertArgs(name, data);
        Object[] results = funcParamsInsert.apply(ptr, args.namePtr, args.dataPtr, (long) data.length);

        if ((int) results[0] != 0) {
            throw new RuntimeException("Error during insert of " + name);
        }
    }

    public byte[] paramsGet(int ptr, String name) {
        var namePtr = storeGetArgs(name);

        var dataPtr = (int) funcParamsParamData.apply(ptr, namePtr)[0];
        var dataLen = (long) funcParamsParamLen.apply(ptr, namePtr)[0];

        if ((dataLen == 0) || (dataPtr == 0)) {
            throw new RuntimeException("Could not find " + name);
        }

        var result = new byte[(int) dataLen];
        var buffer = memory.buffer();
        buffer.position(dataPtr).get(result);

        return result;
    }

    public long paramsLen(int ptr) {
        Object[] results = funcParamsLen.apply(ptr);
        return (Long) results[0];
    }

    private EncodedInsertArgs storeInsertArgs(String name, byte[] data) {
        byte[] encodedName;
        try {
            encodedName = name.getBytes("utf8");
        } catch (UnsupportedEncodingException exc) {
            throw new RuntimeException(exc);
        }

        var bufPtr = allocate((long) encodedName.length + 1 + (long) data.length);

        var nameStart = bufPtr;
        var nameEnd = bufPtr + encodedName.length;
        var dataStart = bufPtr + encodedName.length + 1;

        var buffer = memory.buffer();

        buffer.position(nameStart).put(encodedName);
        buffer.position(nameEnd).put((byte) 0);
        buffer.position(dataStart).put(data);

        return new EncodedInsertArgs(nameStart, dataStart);
    }

    private int storeGetArgs(String name) {
        byte[] encodedName;
        try {
            encodedName = name.getBytes("utf8");
        } catch (UnsupportedEncodingException exc) {
            throw new RuntimeException(exc);
        }

        var bufPtr = allocate((long) encodedName.length + 1);

        var nameStart = bufPtr;
        var nameEnd = bufPtr + encodedName.length;

        var buffer = memory.buffer();

        buffer.position(nameStart).put(encodedName);
        buffer.position(nameEnd).put((byte) 0);

        return nameStart;
    }

    private static class EncodedInsertArgs {
        int namePtr;
        int dataPtr;

        EncodedInsertArgs(int namePtr, int dataPtr) {
            this.namePtr = namePtr;
            this.dataPtr = dataPtr;
        }
    }
}