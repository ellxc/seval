import seval

sev = seval.Seval()

env = {}

while True:
    x = input("> ")
    responses, env = sev.parse_string(x, env)
    for r in responses:
        print(repr(r))
