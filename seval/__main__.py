from seval.repls.get_repl import get_repl
from seval.seval import parse_file
import sys

if __name__ == "__main__":
    if len(sys.argv) > 1:
        for f in sys.argv[1:]:
            parse_file(f)
    else:
        get_repl()()
