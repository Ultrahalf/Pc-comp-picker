#!/usr/bin/env python

import sys
import json
import time
from bson.objectid import ObjectId

from pymongo import MongoClient

mc = MongoClient('localhost', 27017)
db = mc['pccomppicker']
products = db['products']
saved_builds = db['saved_builds']


class JSONEncoder(json.JSONEncoder):
    
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return super(JSONEncoder, self).default(obj)


def get_products(category: str, direction: int):
    '''direction 1 = low to high, direction -1 = high to low'''
    objects = products.find({'category': category}).sort("price", direction)

    list_of_dicts = list()
    for obj in objects:
        list_of_dicts.append(obj)

    return list_of_dicts


def get_product_from_id(product_id: str):
    product = products.find_one({'_id': ObjectId(product_id)})
    if product == None:
        print("dbops.get_product_from_id: No such product id!")
        sys.exit(1)
    return product


def id_exists(product_id: str):
    product = products.find_one({'_id': ObjectId(product_id)})
    return not product == None


def save_build(build_name: str, build_url: str, products: dict):
    build_genesis_time = int(time.time())
    
    # build is purged 90 days after creation
    build_purge_time = build_genesis_time + 90 * 24 * 60 * 60

    field = {
        'build_name': build_name,
        'build_url': build_url,
        'build_genesis_time': build_genesis_time,
        'build_purge_time': build_purge_time,
        'products': products,
    }

    saved_builds.insert_one(field)


def build_url_exists(build_url: str):
    build = saved_builds.find_one({'build_url': build_url})
    return not build == None


def get_build_from_build_url(build_url: str):
    build = saved_builds.find_one({'build_url': build_url})
    if not build:
        # something gone wrong
        sys.exit(1)
    return build
