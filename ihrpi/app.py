#!/bin/python
from ihrpi.factory import create_app

application = create_app()
print(application.url_map)


def main():
    application.run(host='0.0.0.0')


if __name__ == "__main__":
    main()
