# `java_jna` - using the C-ABI wrapper in Java using JNA

The wrapper is found in [`Params.java`](src/main/java/rust_jna/Params.java). It
expects the compiled library to be copied to the correct directory in the
[resources directory](src/main/resources). The usage of the `Params` class is
demonstrated in the [test](src/test/java/rust_jna/ParamsTest.java).

To execute this example, navigate to the project root and run

```bash
python make.py java_jna
```
