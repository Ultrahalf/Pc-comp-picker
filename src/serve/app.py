#!/usr/bin/env python

import os
import math
from markupsafe import escape
from collections import OrderedDict

import pygal
from flask import Flask, render_template, request, jsonify
from flask import flash, url_for, redirect, session

import dbops
import util

app = Flask(__name__)

app.secret_key = util.gen_secret_key()
app.json_encoder = dbops.JSONEncoder

ITEMS_PER_PAGE = 20

COMPONENTS = OrderedDict([
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


@app.route('/')
def index():
    return render_template('index.html', components=COMPONENTS)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/wishlist')
def wishlist():
    if 'wishlist' not in session or not session['wishlist']:
        return render_template('wishlist.html')

    total = util.total_build_cost(session['wishlist'])

    config = pygal.Config()
    config.human_readable = True
    config.style = pygal.style.LightGreenStyle

    chart = pygal.Pie(config, inner_radius=.4)
    chart.title = f"Total Build Cost: ₹{total}"

    for prod in session['wishlist']:
        chart.add(prod['title'], prod['price'])
    price_graph = chart.render_data_uri()

    return render_template('wishlist.html', price_graph=price_graph)


@app.route('/component/<name>', methods=['GET', 'POST'])
def component(name):
    pageno = 1
    if request.method == 'GET' and request.args.get('pageno') != None:
        pageno = int(request.args.get('pageno'))
        products = dbops.get_products(name)

    products = dbops.get_products(name)
    numpages = math.ceil(len(products) / ITEMS_PER_PAGE)

    # gives the products to be displayed on page {pageno}
    data = products[pageno * ITEMS_PER_PAGE - ITEMS_PER_PAGE : pageno * ITEMS_PER_PAGE]

    return render_template(
        'component.html',
        name=name,
        data=data,
        pagelen=ITEMS_PER_PAGE,
        pageno=pageno,
        components=COMPONENTS,
        numpages=numpages,
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


@app.route('/_comparison/<product_id>')
def comparison_toggle(product_id):
    product = dbops.get_product_from_id(product_id)

    if product['vendor'] not in ['itdepot', 'mdcomputer', 'vedant']:
        flash(f"Comparison not available for vendor {product['vendor']}")
        return "incompatible vendor"

    if 'comparison' not in session: # definitely add
        comparison = session.setdefault('comparison', [])
        comparison.append(product)
        session.modified = True
        newbuttontext = "remove"
        return jsonify(newbuttontext=newbuttontext)

    else:   # maybe add, maybe remove
        comparison = session['comparison']
        for prod in comparison:
            if prod['_id'] == product_id:  # definitely remove
                session['comparison'] = [
                    prod for prod in session['comparison'] if not (prod['_id']) == product_id
                ]
                session.modified = True
                return jsonify(newbuttontext="compare")

        # definitely add
        if len(comparison) >= 2:
            flash("Two elements already added for comparison.  Remove one of them if you want to add another.")
            os.system("echo two added")
            return "too many products"
        comparison.append(product)
        session.modified = True
        return jsonify(newbuttontext="compare")


if __name__ == '__main__':
    app.run(debug=True)
