import argparse

ACTIONS_MAP = {"hazzlecast": ""}


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--action", "-a", help="Add action")

    args = parser.parse_args()

    print('args', args)

    # if args.action:


if __name__ == "__main__":
    main()
