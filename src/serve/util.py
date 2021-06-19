#!/usr/bin/env python

import os
import random
import string

import dbops


def gen_wishlist_url() -> str:
    url = ''.join(random.choice(string.ascii_letters) for _ in range(9))
    return f'/wishlist/{url}'


def add_to_wishlist(product_id):
    product = dbops.get_product_with_id(product_id)
    return product


def gen_secret_key():
    return os.urandom(12).hex()


if __name__ == '__main__':
    print(gen_wishlist_url())
    add_to_wishlist('60ccb5ffc3aa12d41a9a9b1b')
