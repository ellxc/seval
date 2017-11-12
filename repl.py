#!/usr/env python3
import atexit
import os
import sys

import readline

import seval
import seval_completer
import seval_env

HISTFILE = os.path.join(os.path.expanduser("~"), "seval_history")


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

        completer = seval_completer.Completer(namespace=env)
        readline.set_completer(completer.complete)
        readline.parse_and_bind('tab: complete')

        self.seval = seval.Seval()
        self.env = env

    def save_history(self):
        """Writes the history to the HISTFILE as setup in __init__"""
        new_h_len = readline.get_history_length()
        readline.set_history_length(1000)
        readline.write_history_file(HISTFILE)

    def built_ins(self, line):
        """Simple parsing for some built in functions."""
        if line == "env":
            print(repr(self.env))
            return True
        if line == "myenv":
            globalenv = seval_env.SevalEnv.globalenv
            myenv = {k: v for k, v in self.env.items() if k not in globalenv}
            print(repr(myenv))
            return True

        elif line == "help":
            print("This is the seval interpretter. Control-D to exit.")
            print("  'env'    Print the whole environment")
            print("  'myenv'  Print the difference between the starting environment and the new environment")
            print("  'help'   Display this message")
            return True
        return False

    def repl(self):
        while True:
            try:
                line = input(">>> ")
                if self.built_ins(line):
                    continue
                else:
                    e, tenv = self.seval.parse_string(line, self.env)
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


            except:
                print('wtf')


if __name__ == "__main__":
    seval_e = seval_env.SevalEnv
    seval_r = SevalTTY(seval_e)
    atexit.register(seval_r.save_history)

    # Print some status information
    print("seval repl")
    print(sys.version)
    print("Control-D to exit.")

    # Start the repl
    seval_r.repl()
