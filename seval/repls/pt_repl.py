#!/usr/bin/env python
"""
"""
import keyword
import sys
import traceback

import six
from prompt_toolkit.shortcuts import create_eventloop
from prompt_toolkit.styles import style_from_pygments
from ptpython.completer import PythonCompleter
from ptpython.python_input import PythonCommandLineInterface, PythonInput
from pygments.lexers.python import PythonTracebackLexer
from pygments.styles.default import DefaultStyle

from seval.seval import parse_string
from seval.constants.global_env import globalenv


class BodgedPythonCompleter(PythonCompleter):
    """this is a nessesary bodge to not add builtins that are not included in the seval env to the suggestions."""

    def get_completions(self, document, complete_event):
        for x in super(BodgedPythonCompleter, self).get_completions(document=document, complete_event=complete_event):
            if "." in document.text:
                name, _, _ = document.text.partition(".")
            else:
                name = x.text
            if name in self.get_globals() or name in self.get_locals() or keyword.iskeyword(name):
                yield x


def _lex_python_traceback(tb):
    """ Return token list for traceback string. """
    lexer = PythonTracebackLexer()
    return lexer.get_tokens(tb)


def _handle_exception(cli, e, style=style_from_pygments(DefaultStyle)):
    output = cli.output

    # Instead of just calling ``traceback.format_exc``, we take the
    # traceback and skip the bottom calls of this framework.
    t, v, tb = sys.exc_info()
    tblist = traceback.extract_tb(tb)

    for line_nr, tb_tuple in enumerate(tblist):
        if tb_tuple[0] == '<stdin>':
            tblist = tblist[line_nr:]
            break

    l = traceback.format_list(tblist)
    if l:
        l.insert(0, "Traceback (most recent call last):\n")
    l.extend(traceback.format_exception_only(t, v))

    # For Python2: `format_list` and `format_exception_only` return
    # non-unicode strings. Ensure that everything is unicode.
    if six.PY2:
        l = [i.decode('utf-8') if isinstance(i, six.binary_type) else i for i in l]

    tb = ''.join(l)

    # Format exception and write to output.
    # (We use the default style. Most other styles result
    # in unreadable colors for the traceback.)
    tokens = _lex_python_traceback(tb)
    cli.print_tokens(tokens, style=style)

    output.write('%s\n' % e)
    output.flush()


def main():
    locals_ = {}
    globals_ = globalenv
    eventloop = create_eventloop()
    try:
        python_input = PythonInput(get_globals=lambda: globals_, get_locals=lambda: locals_,
                                   history_filename=".sevalhist",
                                   _completer=BodgedPythonCompleter(lambda: locals_, lambda: globals_))
        cli = PythonCommandLineInterface(eventloop=eventloop, python_input=python_input)
        while 1:
            python_code = cli.run()
            if python_code.text == "exit":
                break
            try:
                result, env = parse_string(locals_, python_code.text)
                for x in result:
                    print(repr(x))
            except Exception as e:
                _handle_exception(cli=cli, e=e, style=python_input._current_style)
    except EOFError:
        pass
    finally:
        eventloop.close()


if __name__ == '__main__':
    main()
