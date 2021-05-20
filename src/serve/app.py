#!/usr/bin/env python

from flask import Flask, render_template, request

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

@app.route('/component')
def component():
    return render_template('component.html')

if __name__ == '__main__':
    app.run(debug=True)
