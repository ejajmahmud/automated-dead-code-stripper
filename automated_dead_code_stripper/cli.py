"""CLI for automated-dead-code-stripper."""
import sys
import argparse
from .stripper import DeadCodeStripper

def main():
    parser = argparse.ArgumentParser(description="Automated Dead Code Stripper CLI")
    parser.add_argument("--demo", action="store_true", help="Strip unused dead function")
    args = parser.parse_args()

    if args.demo:
        stripper = DeadCodeStripper()
        code = """
def unused_dead_function():
    return "nobody calls me"

def live_helper():
    return "live"

def main():
    print(live_helper())
        """
        res = stripper.strip_dead_code(code, entry_points=["main"])
        print(f"Removed Functions: {res.removed_functions}")
        print(f"Cleaned Code:\n{res.cleaned_code}")
    else:
        parser.print_help()
    sys.exit(0)

if __name__ == "__main__":
    main()
