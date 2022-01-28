package rust_wasm;

public class Params implements AutoCloseable {
    WasmRuntime runtime;
    Integer ptr;

    public Params() {
        this.runtime = WasmRuntime.get();
        this.ptr = runtime.paramsNew();
    }

    public long len() {
        ensurePtr();
        return runtime.paramsLen(ptr);
    }

    public void insert(String name, byte[] data) {
        ensurePtr();
        runtime.paramsInsert(ptr, name, data);
    }

    public byte[] get(String name) {
        ensurePtr();
        return runtime.paramsGet(ptr, name);
    }

    public void close() {
        if (ptr != null) {
            runtime.paramsFree(ptr);
            ptr = null;
        }
    }

    private void ensurePtr() {
        if (ptr == null) {
            throw new RuntimeException("Invalid operation on freed Params instance");
        }
    }
}
