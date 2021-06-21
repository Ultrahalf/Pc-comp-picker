#!/usr/bin/env python

import os
from markupsafe import escape
from collections import OrderedDict

from flask import Flask, render_template, request
from flask import flash, url_for, redirect, session

import dbops
import util

app = Flask(__name__)

app.secret_key = util.gen_secret_key()
app.json_encoder = dbops.JSONEncoder

ITEMS_PER_PAGE = 20


@app.route('/')
def index():
    components = OrderedDict([
        ('CPU', 'cpu'),
        ('Cooling System', 'cooler'),
        ('Motherboard', 'motherboard'),
        ('Memory', 'memory'),
        ('Storage Device', 'storage'),
        ('Case', 'case'),
        ('Power Supply Unit', 'psu'),
        ('Graphic Card', 'gpu'),
        ('Monitor', 'monitor'),
    ])

    return render_template('index.html', components=components)


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
        data = dbops.get_data(ITEMS_PER_PAGE*pageno, name)

    data = dbops.get_data(ITEMS_PER_PAGE*pageno, name)

    return render_template(
        'component.html',
        name=name,
        data=data[-ITEMS_PER_PAGE:],
        pagelen=ITEMS_PER_PAGE,
        pageno=pageno
    )


@app.route('/_add_to_wishlist/<product_id>')
def add_to_wishlist(product_id):
    # Ensure session['wishlist'] is not empty
    session_ = session.setdefault('wishlist', [])

    # Ensure product is not already in the wishlist
    for s in session_:
        if s["_id"] == product_id:
            flash("Product has already been added")
            return "Not added"

    product = dbops.get_product_from_id(product_id)
    session_.append(product)
    session.modified = True
    return "Added"


if __name__ == '__main__':
    app.run(debug=True)
