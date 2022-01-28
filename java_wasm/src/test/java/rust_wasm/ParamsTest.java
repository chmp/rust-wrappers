package rust_wasm;

import java.io.UnsupportedEncodingException;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertArrayEquals;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

public class ParamsTest {
    @Test
    public void testApp() throws UnsupportedEncodingException {
        var encodedData = "world".getBytes("utf8");

        try (var params = new Params()) {
            assertEquals(0, params.len());

            params.insert("hello", encodedData);
            assertEquals(1, params.len());
            assertArrayEquals(encodedData, params.get("hello"));

            assertThrows(RuntimeException.class, () -> params.get("missing"));
        }
    }
}
