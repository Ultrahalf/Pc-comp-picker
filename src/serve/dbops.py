#!/usr/bin/env python

import mongoengine
from mongoengine import connect

connect('pccomppicker')

class Product(mongoengine.Document):
    vendor = mongoengine.StringField(required=True)
    title = mongoengine.StringField(required=True)
    img = mongoengine.StringField(required=True)
    url = mongoengine.StringField(required=True)
    price = mongoengine.StringField(required=True)
    category = mongoengine.StringField(required=True)

    meta = {
        'collection': 'products',
    }
