# seval

`seval` provides a meta-circular Python interpretter for user interaction. It is
designed to safely evaluate python code without allowing calls to access the
underlying operating system.

This is done by evaluation of python expressions under a restricted environment.
Various python libaries are forbidden, and access to private fields is
prohibitted.

```
>>> "".__repr__()
Exception: access to private fields is disallowed
```

## Purpose

`seval` has been designed to provide a programming interface over IRC to enable
writing macros and plugins for [pyperbot](https://github.com/ellxc/pyperbot).

## Installation

This should be no different from any other python module, Seval has no external dependencies.
`pip install git+git://github.com/ellxc/seval`

## Caveat

`seval` has not been formally tested, and may have bugs. It has been implemented
to attempt to ensure safe sandboxed execution, but there could be bugs. Use at
your own risk.

## repl

There is a `repl` using a GNU Readline interface. You'll need a readline
implementation installed from pip. `anyreadline` is a metapackage which installs
a readline library appropriate for your operating system. The `gnureadline`
package is incompatible with Windows. You can get to the repl by executing the
module with the '-m' flag of the python interpretter. `python -m seval`

## file execution

Running whole files can be acheived thusly `python -m seval <filename>`

