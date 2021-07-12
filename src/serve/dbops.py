#!/usr/bin/env python

import sys
import json
from bson.objectid import ObjectId

from pymongo import MongoClient

mc = MongoClient('localhost', 27017)
db = mc['pccomppicker']
products = db['products']


class JSONEncoder(json.JSONEncoder):
    
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return super(JSONEncoder, self).default(obj)


def get_products(category: str, direction: int):
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
