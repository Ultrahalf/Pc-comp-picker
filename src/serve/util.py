#!/usr/bin/env python

import os
import random
import string

import dbops


def gen_wishlist_url() -> str:
    url = ''.join(random.choice(string.ascii_letters) for _ in range(9))
    return f'/wishlist/{url}'


def add_to_wishlist(product_id):
    product = dbops.get_product_from_id(product_id)
    return product


def gen_secret_key():
    return os.urandom(12).hex()


def total_build_cost(wishlist):
    total = 0
    for prod in wishlist:
        total += prod['price']
    return total


# testing
if __name__ == '__main__':
    print(gen_wishlist_url())
