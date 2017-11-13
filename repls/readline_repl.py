#!/usr/env python3
import atexit
import os
import sys

import readline

import seval_env
from repls import readline_completer
from seval import parse_string

# Make the history file hidden on UNIX type operating systems
if sys.platform == "win32":
    HISTFILE = os.path.join(os.path.expanduser("~"), "seval_history")
else:
    HISTFILE = os.path.join(os.path.expanduser("~"), ".seval_history")


class SevalTTY:
    def __init__(self, env):
        """Set up the seval REPL.

        We open a .history file in ~/.config/seval_history, or create
        it if it doesn't exist.

        We then save the build the tab completer with the environment
        passed into the object, and finally save the environment.

        """
        try:
            readline.read_history_file(HISTFILE)
            self.history_length = readline.get_history_length()
        except FileNotFoundError:
            open(HISTFILE, 'wb').close()
            self.history_length = 0

        completer = readline_completer.Completer(namespace=env)
        readline.set_completer(completer.complete)
        readline.parse_and_bind('tab: complete')
        self.built_ins = {
            "print_env": (
                self.toggle_print_env,
                "Toggle printing the environment after each command"
            ),
            "env"      : (
                self.print_env,
                "Print the whole environment"
            ),
            "help"     : (
                self.print_help,
                "Display this message"
            )
        }

        self.env = env

    def save_history(self):
        """Writes the history to the HISTFILE as setup in __init__"""
        new_h_len = readline.get_history_length()
        readline.set_history_length(1000)
        readline.write_history_file(HISTFILE)

    def print_env(self):
        print(repr(self.env))

    def toggle_print_env(self):
        if 'print_env' in self.env:
            self.env['print_env'] = (not self.env['print_env'])
        else:
            self.env['print_env'] = True
        print("print_env = {}".format(self.env['print_env']))

    def print_help(self):
        print("This is the seval interpretter. Control-D to exit.")
        for (k, (_, h)) in self.built_ins.items():
            print("  {:15s} {}".format(k, h))

    def parse_builtins(self, line):
        """Simple parsing for some built in functions."""
        for (k, v) in self.built_ins.items():
            if k == line:
                v[0]()
                return True
        return False

    def repl(self):
        while True:
            try:
                line = input(">>> ")
                if self.parse_builtins(line):
                    continue
                else:
                    e, tenv = parse_string(line, self.env)
                    if ('print_env' in tenv and tenv['print_env']):
                        print(tenv)
                    self.env.update(tenv)
                for exp in e:
                    print("{}: {}".format(type(exp).__name__, repr(exp)))

            except SyntaxError as e:
                print("Syntax error.")
                print("{}\n{}^".format(e.text, " " * (e.offset)))
                print(e)

            except KeyboardInterrupt:
                print("Interrupt.")

            except EOFError:
                # On EOF (Control-D) break the loop.
                print("Exiting.\n")
                self.save_history()
                break

            except Exception as e:
                print("{}: {}".format(type(e).__name__, e))


def main():
    seval_e = seval_env.SevalEnv
    seval_r = SevalTTY(seval_e)
    atexit.register(seval_r.save_history)

    # Print some status information
    print("seval repl")
    print(sys.version)
    print("Control-D to exit.")

    # Start the repl
    seval_r.repl()


if __name__ == "__main__":
    main()
