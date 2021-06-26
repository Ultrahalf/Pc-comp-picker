#!/usr/bin/env python

import os
from markupsafe import escape
from collections import OrderedDict

from flask import Flask, render_template, request, jsonify
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
        pageno=pageno,
    )


@app.route('/_add_to_wishlist/<product_id>')
def add_to_wishlist(product_id):
    # Create session['wishlist'] if it doesn't exist
    wishlist = session.setdefault('wishlist', [])

    # Ensure product is not already in the wishlist
    for prod in wishlist:
        if prod['_id'] == product_id:
            flash("Product has already been added")
            return jsonify(message="Failed to add")

    product = dbops.get_product_from_id(product_id)
    wishlist.append(product)
    session.modified = True
    return jsonify(newtext="Remove from Wishlist", newid=f"remove-{product_id}")


@app.route('/_remove_from_wishlist/<product_id>')
def remove_from_wishlist(product_id):
    # Ensure session['wishlist'] exists
    if 'wishlist' not in session:
        return "Failed to Remove"

    session['wishlist'] = [prod for prod in session['wishlist'] if not (prod['_id']) == product_id]
    session.modified = True
    return jsonify(newtext="Add to Wishlist", newid=f"add-{product_id}")


@app.route('/_wishlist_toggle/<product_id>')
def wishlist_toggle(product_id):
    if 'wishlist' not in session:           # definitely add
        wishlist = session.setdefault('wishlist', [])
        product = dbops.get_product_from_id(product_id)
        wishlist.append(product)
        session.modified = True
        return jsonify(
            message="change button to remove",
            newbuttonid=f"remove-{product_id}",
            newbuttonclass="btn-remove",
            newbuttontext="remove from wishlist",
        )

    else:                                   # maybe add, maybe remove
        wishlist = session['wishlist']
        for prod in wishlist:
            if prod['_id'] == product_id:   # definitely remove
                session['wishlist'] = [
                    prod for prod in session['wishlist'] if not (prod['_id']) == product_id
                ]
                session.modified = True
                return jsonify(
                    message="change button to add",
                    newbuttonid=f"add-{product_id}",
                    newbuttonclass="btn-add",
                    newbuttontext="add to wishlist",
                )
        # definitely add
        product = dbops.get_product_from_id(product_id)
        wishlist.append(product)
        session['wishlist'] = sorted(session['wishlist'], key=lambda k: k['url']) 
        session.modified = True
        return jsonify(
            message="change button to remove",
            newbuttonid=f"remove-{product_id}",
            newbuttonclass="btn-remove",
            newbuttontext="remove from wishlist",
        )


if __name__ == '__main__':
    app.run(debug=True)
