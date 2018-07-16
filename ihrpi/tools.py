try:
    import configparser
except ImportError:
    import ConfigParser as configparser


def get_current_version():
    config = configparser.ConfigParser()
    config.read('.bumpversion.cfg')
    cv = config.get('bumpversion', 'current_version')
    if config.has_option('bumpversion', 'tag_name'):
        return config.get('bumpversion', 'tag_name').format(new_version=cv)
    else:
        return "v"+cv


def gcv_main():
    """doing this because fn gets parsed like so:
       https://packaging.python.org/specifications/entry-points/#use-for-scripts""" # noqa
    print(get_current_version())
    return 0
