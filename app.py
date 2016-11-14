import client
import sys


def main(args):
    """
    Instantiate app.
    """
    if args[1] == '--player':
        movegen = client.MoveGeneratorPlayer()
    else:
        movegen = client.MoveGeneratorAI()
    app = client.Client(movegen)
    app.run()


if __name__ == "__main__":
    main(sys.argv)

