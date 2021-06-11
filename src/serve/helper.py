#!/usr/bin/env python

import random, string

def gen_wishlist_url() -> str:
    url = ''.join(random.choice(string.ascii_letters) for _ in range(9))
    return f'/wishlist/{url}'


if __name__ == '__main__':
    print(gen_wishlist_url())
