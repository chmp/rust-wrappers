from os import path
import pathlib
import shutil
import subprocess
import sys

self_path = pathlib.Path(__file__).parent.resolve()


def main():
    run("cargo", "build", "--package", "pyo3_wrapper")
    cp(
        self_path / "target" / "debug" / "libpyo3_wrapper.so",
        self_path / "python_pyo3" / "pyo3_wrapper.so",
    )
    python("python_usage.py", cwd=self_path / "python_pyo3")


def cp(src, dst):
    print("cp", str(src), str(dst))
    shutil.copy(src, dst)


def run(*args, check=True, **kwargs):
    args = [str(arg) for arg in args]
    print("run", *args)
    subprocess.run(args, check=check, **kwargs)


def python(*args, **kwargs):
    run(sys.executable, *args, **kwargs)


if __name__ == "__main__":
    main()
