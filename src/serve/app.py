#!/usr/bin/env python

import os

from flask import Flask, render_template, request
from flask import flash, url_for, redirect

import dbops

app = Flask(__name__)

ITEMS_PER_PAGE = 20


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/wishlist')
def wishlist():
    return render_template('wishlist.html')


@app.route('/component/<name>', methods=['GET', 'POST'])
def component(name):
    pageno = 1
    if request.method == 'GET' and request.args.get('pageno') != None:
        pageno = int(request.args.get('pageno'))
        data = get_data(ITEMS_PER_PAGE*pageno)

    if name == 'memory':
        data = get_data(ITEMS_PER_PAGE*pageno)
        return render_template('component.html', name=name, data=data[-ITEMS_PER_PAGE:], pagelen=ITEMS_PER_PAGE, pageno=pageno)


def get_data(pagelen):
    objects = dbops.Product.objects.limit(pagelen)

    list_of_dicts = list()
    for obj in objects:
        vendor  = obj.vendor
        title   = obj.title
        img     = obj.img
        url     = obj.url
        price   = obj.price

        list_of_dicts.append(
            {'vendor':vendor, 'title':title, 'img':img, 'url':url, 'price':price}
        )

    return list_of_dicts


if __name__ == '__main__':
    app.run(debug=True)
