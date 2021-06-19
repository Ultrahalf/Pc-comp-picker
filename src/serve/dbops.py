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


def get_data(pagelen: int, category: str):
    objects = products.find({'category': category}).limit(pagelen)

    list_of_dicts = list()
    for obj in objects:
        list_of_dicts.append(obj)

    return list_of_dicts


def get_product_with_id(product_id):
    product = products.find_one({'_id': ObjectId(product_id)})
    if product == None:
        print("No such product id!")
        sys.exit(1)
    return product


if __name__ == '__main__':
    prod = get_product_with_id('60ccb5ffc3aa12d41a9a9b1b')
    print(prod['title'])
