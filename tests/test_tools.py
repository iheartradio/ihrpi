import os

from posixpath import join
from ihrpi import tools

class TestTools:

    def get_test_file(self, v, tag_name):
        return """
[bumpversion]
current_version = {}
commit = True
tag = True
{}

[bumpversion:file:setup.py]

""".format(v, tag_name if tag_name is not None else '')

    def test_get_current_version(self, tmpdir):
        p = join(tmpdir, '.bumpversion.cfg')
        os.chdir(tmpdir)

        v = '0.1.0'
        prefix = 'my_version'
        for expected, t in [('v'+v, ''),
                            (prefix+v, 'tag_name = %s{new_version}'%prefix)]:
            with open(p, 'w') as f: 
                f.write(self.get_test_file(v, t)) 
            actual = tools.get_current_version()
            assert expected == actual
