import client


def main():
    """
    Instantiate app.
    """
    app = client.Client(client.MoveGeneratorPlayer())
    app.run()


if __name__ == "__main__":
    main()

