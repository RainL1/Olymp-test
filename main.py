import argparse
import shlex
import subprocess
import sys
from pathlib import Path
from tempfile import TemporaryDirectory


def get_command(file: str, name: str, tmp: str) -> list[str]:
    path = Path(file)
    if not path.exists():
        raise FileNotFoundError(f"Source file not found: {file}")

    if path.suffix == ".cpp":
        exe = Path(tmp) / name
        subprocess.run(["g++", file, "-O2", "-std=c++17", "-o", str(exe)], check=True)
        return [str(exe)]
    if path.suffix == ".py":
        return [sys.executable, file]
    return shlex.split(file)


def run(command: list[str], data: str = "") -> str:
    return subprocess.run(
        command,
        input=data,
        text=True,
        capture_output=True,
        check=True,
    ).stdout.strip()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--gen", default="user.py")
    parser.add_argument("--good", default="good.cpp")
    parser.add_argument("--bad", default="bad.cpp")
    parser.add_argument("--tests", type=int, default=1000)
    args = parser.parse_args()

    with TemporaryDirectory() as tmp:
        gen = get_command(args.gen, "gen", tmp)
        good = get_command(args.good, "good", tmp)
        bad = get_command(args.bad, "bad", tmp)

        for i in range(1, args.tests + 1):
            test = run(gen)
            gout = run(good, test)
            bout = run(bad, test)

            if gout != bout:
                print(f"Test #{i}: DIFF")
                print("Input:")
                print(test)
                print("Good:")
                print(gout)
                print("Bad:")
                print(bout)
                return

            print(f"Test #{i}: OK")

    print("No differences found.")


if __name__ == "__main__":
    main()
