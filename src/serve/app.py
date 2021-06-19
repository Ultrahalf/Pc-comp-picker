#!/usr/bin/env python

import os

from flask import Flask, render_template, request
from flask import flash, url_for, redirect, session

import dbops
import util

app = Flask(__name__)

ITEMS_PER_PAGE = 100

app.secret_key = util.gen_secret_key()
app.json_encoder = dbops.JSONEncoder


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/wishlist')
def wishlist():
    product_id = '60ccb5ffc3aa12d41a9a9b1b'
    product = util.add_to_wishlist(product_id)
    session['wish'] = product
    session.modified = True
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


if __name__ == '__main__':
    app.run(debug=True)
