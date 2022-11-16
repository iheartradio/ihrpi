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
    , 'wheel'
]

setup(
    name='ihrpi',
    version='1.2.0',
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
    install_requires=[
        # See https://github.com/getsentry/responses/blob/df920c09fcdb97f260dddba631ad5a1d9042188a/CHANGES#L45
        # We need the `_is_string` method
        'responses<0.18.0',
        'urllib3>=1.21.1,<1.27',
    ],
    extras_require={
        'api': api
        , 'tools': tools
    },
    packages=find_packages(exclude=['tests'])
)
