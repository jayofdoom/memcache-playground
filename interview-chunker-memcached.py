#!/usr/bin/python

import hashlib
import sys

from pymemcache.client.base import Client

CHUNK_SIZE = 1000 * 1024

def _get_client():
    return Client(('localhost', 11211))

def _get_digest(file_obj):
    file_obj.seek(0,0)
    m = hashlib.sha256()
    m.update(file_obj.read())
    return m.hexdigest()

def _verify_file(name, file_obj):
    file_digest = _get_digest(file_obj)
    client = _get_client()
    good_digest = client.get(name + 'digest')
    print('original digest: ' + good_digest)
    print('digest of file in memcache: ' + file_digest)
    return good_digest == file_digest

def set_file(name, file_obj):
    client = _get_client()
    m = hashlib.sha256()
    i = 0
    while True:
        chunk = file_obj.read(CHUNK_SIZE)

        if chunk == '':
            break

        client.set(name + str(i), chunk)
        m.update(chunk)
        i += 1

    client.set(name + 'index', i)
    client.set(name + 'digest', str(m.hexdigest()))

def get_file(name, file_obj):
    client = _get_client()
    i = 0
    #TODO: Handle bogus names
    num_chunks = client.get(name + 'index')
    for i in range(int(num_chunks)):
        file_obj.write(client.get(name + str(i)))

with open('bigfile') as f:
    set_file('bigfile', f)

with open('newfile', 'w') as f:
    get_file('bigfile', f)

with open('newfile', 'r') as f:
    _verify_file('bigfile', f)

sys.exit(0)




