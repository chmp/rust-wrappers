package rust_jna;

import java.util.Collections;

import com.sun.jna.Library;
import com.sun.jna.Native;
import com.sun.jna.Pointer;

public class Params implements AutoCloseable {
    Pointer ptr;

    public Params() {
        this.ptr = RustCLib.INSTANCE.params_new();
    }

    public long len() {
        ensurePtr();
        return RustCLib.INSTANCE.params_len(ptr);
    }

    public void insert(String name, byte[] data) {
        ensurePtr();
        RustCLib.INSTANCE.params_insert(ptr, name, data, (long) data.length);
    }

    public byte[] get(String name) {
        ensurePtr();
        var data_length = RustCLib.INSTANCE.params_param_len(ptr, name);
        var data_ptr = RustCLib.INSTANCE.params_param_data(ptr, name);

        if ((data_length == 0) || (data_ptr == Pointer.NULL)) {
            throw new RuntimeException("Could not find key");
        }

        return data_ptr.getByteArray(0, (int) data_length);
    }

    public void close() {
        if (ptr != null) {
            RustCLib.INSTANCE.params_free(ptr);
            ptr = null;
        }
    }

    private void ensurePtr() {
        if (ptr == null) {
            throw new RuntimeException("Invalid operation on freed Params instance");
        }
    }
}

interface RustCLib extends Library {
    RustCLib INSTANCE = (RustCLib) Native.load("rust_clib.so", RustCLib.class,
            Collections.singletonMap(Library.OPTION_STRING_ENCODING, "UTF-8"));

    Pointer params_new();

    void params_free(Pointer ptr);

    byte params_insert(Pointer ptr, String name, byte[] data_ptr, long data_len);

    long params_len(Pointer ptr);

    long params_param_len(Pointer ptr, String name);

    Pointer params_param_data(Pointer ptr, String name);
}
