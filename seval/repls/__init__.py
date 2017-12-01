def get_repl():
    import sys
    if sys.stdin.isatty():
        try:
            from .pt_repl import main as repl
        except ImportError:
            try:
                from .readline_repl import main as repl
            except ImportError:
                from .basic_repl import main as repl
    else:
        try:
            from .readline_repl import main as repl
        except ImportError:
            from .basic_repl import main as repl

    return repl
