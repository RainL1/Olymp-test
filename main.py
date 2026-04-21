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


def run(command: list[str], data: str, timeout: float) -> tuple[int, str, str]:
    proc = subprocess.run(
        command,
        input=data,
        text=True,
        capture_output=True,
        timeout=timeout,
    )
    return proc.returncode, proc.stdout.strip(), proc.stderr


def save_failure(test: str, gout: str, bout: str) -> None:
    Path("failed_input.txt").write_text(test)
    Path("good_out.txt").write_text(gout + "\n")
    Path("bad_out.txt").write_text(bout + "\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--gen", default="user.py")
    parser.add_argument("--good", default="good.cpp")
    parser.add_argument("--bad", default="bad.cpp")
    parser.add_argument("--tests", type=int, default=1000)
    parser.add_argument("--timeout", type=float, default=5.0)
    args = parser.parse_args()

    with TemporaryDirectory() as tmp:
        gen = get_command(args.gen, "gen", tmp)
        good = get_command(args.good, "good", tmp)
        bad = get_command(args.bad, "bad", tmp)

        for i in range(1, args.tests + 1):
            _, test, _ = run(gen, "", args.timeout)

            try:
                grc, gout, gerr = run(good, test, args.timeout)
            except subprocess.TimeoutExpired:
                print(f"\nTest #{i}: good TLE (> {args.timeout}s)")
                save_failure(test, "", "")
                return

            try:
                brc, bout, berr = run(bad, test, args.timeout)
            except subprocess.TimeoutExpired:
                print(f"\nTest #{i}: bad TLE (> {args.timeout}s)")
                save_failure(test, gout, "")
                return

            if grc != 0 or brc != 0 or gout != bout:
                print(f"\nTest #{i}: DIFF (good rc={grc}, bad rc={brc})")
                print("Input:")
                print(test)
                print("Good:")
                print(gout)
                if gerr:
                    print("Good stderr:")
                    print(gerr, end="")
                print("Bad:")
                print(bout)
                if berr:
                    print("Bad stderr:")
                    print(berr, end="")
                save_failure(test, gout, bout)
                return

            print(f"\rTest #{i}: OK", end="", flush=True)

    print(f"\nNo differences found in {args.tests} tests.")


if __name__ == "__main__":
    main()
