#!/usr/bin/python

from pymemcache.client.base import Client

client = Client(('localhost', 11211))
client.set('JayF', 'awesome')
print(client.get('JayF'))
