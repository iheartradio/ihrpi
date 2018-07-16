import boto3
import itertools
import logging
import re

from flask_httpauth import HTTPBasicAuth
from werkzeug.security import check_password_hash
from botocore.client import Config
from botocore.exceptions import ClientError

from os.path import join, basename
from flask import Blueprint, current_app, Response

auth = HTTPBasicAuth()
bp = Blueprint('ihrpi', __name__)

CHUNK_SIZE = 1024

HTML_LINK_PREFIX = '<a href="/simple/{key}/">{key}</a></br>'
HTML_LINK_FILE = '<a href="/simple/{0}">{1}</a></br>'


@auth.get_password
def get_pw(username):
    users = current_app.config['USERS']
    if username in users:
        return users.get(username)
    return None


@auth.verify_password
def verify_password(username, password):
    users = current_app.config['USERS']
    if username in users:
        return check_password_hash(users.get(username), password)
    return False


def _get_client():
    return boto3.client('s3', config=Config(signature_version='s3v4'))


def _handle_client_error(e, path):
    logging.error('Error calling s3_proxy', path, e)
    if e.response['Error']['Code'] == 'NoSuchKey':
        return Response(e.response['Error']['Message'], status=404)
    else:
        return Response(e.response['Error']['Message'], status=500)


def _generate(result):
    """Support generator for s3 response.

    See:
    https://github.com/boto/boto3/issues/426#issuecomment-184889230
    """
    for chunk in iter(lambda: result['Body'].read(CHUNK_SIZE), b''):
        yield chunk


def get_bucket():
    return current_app.config['BUCKET']


def get_prefix():
    return current_app.config['PREFIX']


@bp.route('/ping')
@auth.login_required
def ping():
    return "pong"


def _match_suffix(s):
    p = '^.*\.tar\.gz$|^.*\.zip$|^.*\.egg|^.*\.whl$'
    return re.match(p, s)


def paginate(client, b, p, fmt):
    paginator = client.get_paginator('list_objects')
    p = p+"/"
    s = set()
    for result in paginator.paginate(Bucket=b, Prefix=p):
        for key in result.get('Contents', []):
            k = key.get('Key')[len(p):].split('/')[0]
            if k not in s:
                s.add(k)
                yield fmt.format(key=k)


def paginate_files(client, b, prefix, p, fmt):
    offset = len(p)+1
    link_offset = len(prefix)+1
    paginator = client.get_paginator('list_objects')
    for result in paginator.paginate(Bucket=b, Prefix=p):
        for key in result.get('Contents', []):
            yield fmt.format(key.get('Key')[link_offset:],
                             key.get('Key')[offset:])


@bp.route('/simple', strict_slashes=False)
@auth.login_required
def s3_list_bucket():
    b = get_bucket()
    prefix = get_prefix()
    s3_client = _get_client()
    try:
        logging.info("List bucket: %s", b)
        return Response(paginate(s3_client, b, prefix, HTML_LINK_PREFIX),
                        mimetype='text/html')
    except ClientError as e:
        _handle_client_error(e, prefix)


def _peek(iterable):
    try:
        first = next(iterable)
    except StopIteration:
        return None
    return itertools.chain([first], iterable)


@bp.route('/simple/<path:path>')
@auth.login_required
def s3_proxy(path=None):
    try:
        b = get_bucket()
        prefix = get_prefix()
        p = join(prefix, path)

        logging.info("Getting bucket: %s - key: %s", b, p)
        s3_client = _get_client()
        is_match = _match_suffix(p)
        if is_match:
            s3_res = s3_client.get_object(Bucket=b, Key=p)
            headers = {'Content-Disposition':
                       'attachment;filename=' + basename(p)}
            return Response(_generate(s3_res), mimetype='application/zip',
                            headers=headers)
        else:
            iter = _peek(
                paginate_files(s3_client, b, prefix, p, HTML_LINK_FILE))
            if iter:
                return Response(iter, mimetype='text/html')
            else:
                return Response('No path matches: %s' % path, status=404)
    except ClientError as e:
        _handle_client_error(e, path)
