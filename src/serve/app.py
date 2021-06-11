#!/usr/bin/env python

from flask import Flask, render_template, request

import dbops

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/wishlist')
def wishlist():
    return render_template('wishlist.html')


@app.route('/component/<name>')
def component(name):
    if name == 'memory':
        data = get_data()
        return render_template('component.html', name=name, data=data)


def get_data():
    objects = dbops.Product.objects

    list_of_dicts = list()
    for i in range(0, len(objects)):
        vendor  = objects[i].vendor
        title   = objects[i].title
        img     = objects[i].img
        url     = objects[i].url
        price   = objects[i].price

        list_of_dicts.append(
            {'vendor':vendor, 'title':title, 'img':img, 'url':url, 'price':price}
        )

    return list_of_dicts


if __name__ == '__main__':
    app.run(debug=True)
