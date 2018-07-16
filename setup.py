from setuptools import setup, find_packages

api = [
    'boto3'
    , 'flask >= 0.10.1'
    , 'uwsgi'
    , 'Flask-HTTPAuth'
    , 'dscommons'
]
tools = [
    'awscli'
    , 'bumpversion'
    , 'pip2pi'
    , 'tox'
    , 'pip-tools'
]

setup(
    name='ihrpi',
    version='1.0.0',
    author='Sam Garrett',
    author_email='samgarrett@iheartmedia.com',
    description='iHeart private packaging tools & index.',
    scripts=[
        'bin/ihrpi-build',
        'bin/ihrpi-configure-travis',
        'bin/ihrpi-gen-requirements',
        'bin/ihrpi-publish',
        'bin/ihrpi-release',
        'bin/ihrpi-setup-env',
        'bin/ihrpi-tox-install',
        'bin/ihrpi-tox-run',
    ],
    entry_points={
        'console_scripts': ['ihrpi-gcv=ihrpi.tools:gcv_main'],
    },
    extras_require={
        'api': api
        , 'tools': tools
    },
    packages=find_packages(exclude=['tests'])
)
