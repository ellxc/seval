from seval import parse_string
from seval_env import SevalEnv


def main():
    env = SevalEnv

    while True:
        x = input("> ")
        responses, env = parse_string(env, x)
        for r in responses:
            print(repr(r))


if __name__ == "__main__":
    main()
