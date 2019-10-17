# ihrpi 🍒🍏
> iHeart private packaging tools & index

[![Build Status](https://travis-ci.com/iheartradio/ihrpi.svg?token=DRZy5ZWDwtAusJJ7MRfF&branch=master)](https://travis-ci.com/iheartradio/ihrpi)
[![CircleCI](https://circleci.com/gh/iheartradio/ihrpi/tree/master.svg?style=svg)](https://circleci.com/gh/iheartradio/ihrpi/tree/master)

## Setup for building and installing private packages

1. `git clone git@github.com:iheartradio/ihrpi.git`
2. `cd ihrpi/ && python setup.py install` this will install ihrpi and setup cli
   tools under [bin](https://github.com/iheartradio/ihrpi/tree/master/bin)
3. Assemble values for `IHRPI_HOST`, `IHRPI_USER`, and `IHRPI_PASS`
4. `ihrpi-setup-env` to setup pip.conf with `IHRPI_*` values from previous step
5. `pip install ihrpi[tools]` if you plan to use the cli tools

## Configuration

Basic application file is provided. See [`create_app()`](https://github.com/iheartradio/ihrpi/blob/master/ihrpi/app.py) for setting s3 bucket
and prefix.

## Tools

### Releasing & Pushing packages to your ihrpi from your local machine

    # In your python project of choice:

    cd my_project/
    ihrpi-release
    ihrpi-publish

### Installing packages from ihrpi

    pip install 'mypkg>=0.17.0' \
        --extra-index-url ${IHRPI_URL} \
        --trusted-host ${IHRPI_HOST}

### Access ihrpi from travis build

Travis can be configured to access the private package index. Be careful to not
leak the credentials for ihrpi in travis build logs.

#### Setup

    cd my_project/
    ihrpi-configure-travis

    # tox.ini sections should have:
    install_command =
        ihrpi-tox-install {opts} {packages}

    # .travis.yml install section should include:
    install:
        - git clone git@github.com:iheartradio/ihrpi.git && cd ihrpi/ && python setup.py install && cd ..

    # .travis.yml script section should be:
    script:
        - ihrpi-tox-run

## FAQ

Should I be careful when using tox and the `IHRPI_*` env variables on travis?

    Yes!! tox spews configuration parameters to stdout including the entire
    environment when a run doesn't succeed. This is why `ihrpi-tox-run` and
    `ihrpi-tox-install` scripts are used.

## API

ihrpi API is a flask app serving an s3 bucket formatted to the pypi
[simple specification](https://www.python.org/dev/peps/pep-0503/). We use
`pip2pi` to handle formatting when we run `ihrpi-publish`.

### Debug

This curl should return "pong" from each environment:

    curl "http://${IHRPI_USER}:${IHRPI_PASS}@${IHRPI_HOST}:8089/ping"
