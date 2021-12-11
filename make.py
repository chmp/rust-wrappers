import argparse
import pathlib
import shutil
import subprocess
import sys

self_path = pathlib.Path(__file__).parent.resolve()

_se = lambda effect: lambda f: [f, effect(f)][0]
_gd = lambda o: vars(o).setdefault("__make__", {})
cmd = lambda **kw: _se(lambda f: _gd(f).update(kw))
arg = lambda *a, **k: _se(lambda f: _gd(f).setdefault("__args__", []).append((a, k)))


@cmd(name="all")
def main_all():
    main_rust_test()
    main_python_pyo3()
    main_python_ctypes()


@cmd(name="precommit")
def main_precommit():
    main_format()
    main_all()


@cmd(name="format")
def main_format():
    cargo("fmt")
    python(
        "-m",
        "black",
        "make.py",
        "python_ctypes/rust_clib.py",
        "python_ctypes/python_usage.py",
        "python_pyo3/python_usage.py",
    )


@cmd(name="python_pyo3")
def main_python_pyo3():
    cargo("build", "--package", "pyo3_wrapper")
    cp(
        self_path / "target" / "debug" / "libpyo3_wrapper.so",
        self_path / "python_pyo3" / "pyo3_wrapper.so",
    )
    python("python_usage.py", cwd=self_path / "python_pyo3")


@cmd(name="python_ctypes")
def main_python_ctypes():
    cargo("build", "--package", "rust_clib")
    cp(
        self_path / "target" / "debug" / "librust_clib.so",
        self_path / "python_ctypes" / "_rust_clib.so",
    )
    python("python_usage.py", cwd=self_path / "python_ctypes")


@cmd(name="rust_test")
def main_rust_test():
    cargo("test")
    cargo("clippy")


def cp(src, dst):
    print("cp", str(src), str(dst))
    shutil.copy(src, dst)


def run(*args, check=True, cwd=self_path, **kwargs):
    args = [str(arg) for arg in args]
    print("run", *args)
    subprocess.run(args, check=check, cwd=cwd, **kwargs)


def cargo(*args, **kwargs):
    run("cargo", *args, **kwargs)


def python(*args, **kwargs):
    run(sys.executable, *args, **kwargs)


def main():
    parser = _build_parser()
    args = vars(parser.parse_args())

    if "__main__" not in args:
        return parser.print_help()

    func = args.pop("__main__")
    return func(**args)


def _build_parser():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    for func in globals().values():
        if not hasattr(func, "__make__"):
            continue

        desc = dict(func.__make__)
        name = desc.pop("name", func.__name__)
        args = desc.pop("__args__", [])

        subparser = subparsers.add_parser(name, **desc)
        subparser.set_defaults(__main__=func)

        for arg_args, arg_kwargs in args:
            subparser.add_argument(*arg_args, **arg_kwargs)

    return parser


if __name__ == "__main__":
    main()
