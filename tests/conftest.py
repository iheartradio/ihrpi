import boto3
import pytest

from werkzeug.security import generate_password_hash
from ihrpi import factory
from mock import patch
from moto import mock_s3

@pytest.fixture(scope="session")
def s3_resource(request):
    mock = mock_s3()
    mock.start()
    s3r = boto3.resource('s3', region_name='us-east-1')
    request.addfinalizer(lambda: mock.stop())
    return s3r


@pytest.fixture(autouse=True)
def app(request, monkeypatch):
    p = 'plain_pass'
    monkeypatch.setattr(factory, '_get_users', lambda: {
        'basic_user': generate_password_hash(p)
    })
    config = {
        'TESTING': True,
        'BUCKET': 'ihr-local',
        'PREFIX': 'packages/simple',
        'PLAIN_PASS': p
    }
    app = factory.create_app(config=config)
    with app.app_context():
        yield app


@pytest.fixture
def client(request, app):

    client = app.test_client()

    return client
