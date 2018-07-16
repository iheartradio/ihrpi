import boto3
import pytest
import six

from base64 import b64encode
from os.path import join
from requests.auth import HTTPBasicAuth

class TestBase:

    @classmethod
    def get_auth_headers(cls, u, p):
        s = "{0}:{1}".format(u, p)
        return {
            'Authorization': 'Basic %s' % b64encode(bytes(s, "utf-8")).decode("ascii")
        }


    @pytest.fixture(autouse=True)
    def setup_method(self, tmpdir, app, s3_resource):
        bucket = app.config['BUCKET']
        prefix = app.config['PREFIX']
        (user, _) = list(app.config['USERS'].items())[0]
        p = app.config['PLAIN_PASS']
        self.auth_headers = self.get_auth_headers(user, p)
        self.pkg_names = ["bye", "hi"]
        self.base = "simple"
        s3_resource.create_bucket(Bucket=bucket)

        self.n_versions = 3
        self.pkg_val = []
        self.key = []
        s3_client = boto3.client('s3')
        for pkg in self.pkg_names:
            for i in range(self.n_versions):
                self.pkg_val.append("{}_{}".format(pkg, i))
                self.key.append("{}-0.{}.0.tar.gz".format(pkg, i))
                s3_client.put_object(Bucket=bucket,
                                     Key=join(prefix, pkg, self.key[i]),
                                     Body=self.pkg_val[i])


    def test_ping(self, client):
        r = client.get('/ping',
                       headers=self.auth_headers)
        assert six.b('pong') in r.data


    def test_basic(self, app, client):
        r = client.get(join(self.base, self.pkg_names[0], self.key[0]),
                       headers=self.auth_headers)
        assert six.b(self.pkg_val[0]) == r.data


    def test_top_level_list(self, app, client):
        r = client.get("/"+self.base+"/",
                       headers=self.auth_headers)
        for n in self.pkg_names:
            expect = six.b("a href=\"/{base}/{n}/\">{n}<".format(
                base=self.base, n=n))
            assert expect in r.data


    def test_basic_list(self, app, client):
        pkg = self.pkg_names[0]
        r = client.get(join(self.base, pkg),
                       headers=self.auth_headers)
        for idx, fname in enumerate(self.key[:self.n_versions]):
            expect = six.b("a href=\"/{base}/{pkg}/{fname}\">{fname}<".format(
                base=self.base, pkg=pkg, fname=fname))
            assert expect in r.data


    def test_not_found(self, app, client):
        r = client.get(join(self.base, "blah"),
                       headers=self.auth_headers)
        assert 404 == r.status_code
