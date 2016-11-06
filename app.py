import client


def main():
    """
    Instantiate app.
    """
    movegen = client.MoveGeneratorPlayer()
    app = client.Client(movegen)
    app.run()


if __name__ == "__main__":
    main()

