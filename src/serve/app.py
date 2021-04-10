#!/usr/bin/env python

from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def component(sql=''):
    pl = request.form.get('price-low')
    ph = request.form.get('price-high')
    cpu = request.form.get('cpu-check')
    ram = request.form.get('ram-check')
    gpu = request.form.get('gpu-check')
    amz = request.form.get('amazon-check')
    mdc = request.form.get('mdcomputers-check')
    csp = request.form.get('computerspace-check')
    vdn = request.form.get('vedantcomputers-check')
    prm = request.form.get('primeabgb-check')
    itd = request.form.get('itdepot-check')
    sql_strings = ""
    if (cpu == 'on'):
        sql_strings += "SELECT * FROM cpu WHERE "
        if (amz == 'on'):
            sql_strings += "vendor=amazon "
        if (mdc == 'on'):
            if sql_strings.split()[-1] != 'WHERE':
                sql_strings += "AND "
            sql_strings += "vendor=mdcomputers "
        if (csp == 'on'):
            if sql_strings.split()[-1] != 'WHERE':
                sql_strings += "AND "
            sql_strings += "vendor=computerspace "
        if (vdn == 'on'):
            if sql_strings.split()[-1] != 'WHERE':
                sql_strings += "AND "
            sql_strings += "vendor=vedantcomputers "
        if (prm == 'on'):
            if sql_strings.split()[-1] != 'WHERE':
                sql_strings += "AND "
            sql_strings += "vendor=primeabgb "
        if (itd == 'on'):
            if sql_strings.split()[-1] != 'WHERE':
                sql_strings += "AND "
            sql_strings += "vendor=itdepot "
    if (gpu == 'on'):
        sql_strings += "------------SELECT * FROM ram WHERE "
        if (amz == 'on'):
            sql_strings += "vendor=amazon "
        if (mdc == 'on'):
            if sql_strings.split()[-1] != 'WHERE':
                sql_strings += "AND "
            sql_strings += "vendor=mdcomputers "
        if (csp == 'on'):
            if sql_strings.split()[-1] != 'WHERE':
                sql_strings += "AND "
            sql_strings += "vendor=computerspace "
        if (vdn == 'on'):
            if sql_strings.split()[-1] != 'WHERE':
                sql_strings += "AND "
            sql_strings += "vendor=vedantcomputers "
        if (prm == 'on'):
            if sql_strings.split()[-1] != 'WHERE':
                sql_strings += "AND "
            sql_strings += "vendor=primeabgb "
        if (itd == 'on'):
            if sql_strings.split()[-1] != 'WHERE':
                sql_strings += "AND "
            sql_strings += "vendor=itdepot "
    if (ram == 'on'):
        sql_strings += "------------SELECT * FROM gpu WHERE "
        if (amz == 'on'):
            sql_strings += "vendor=amazon "
        if (mdc == 'on'):
            if sql_strings.split()[-1] != 'WHERE':
                sql_strings += "AND "
            sql_strings += "vendor=mdcomputers "
        if (csp == 'on'):
            if sql_strings.split()[-1] != 'WHERE':
                sql_strings += "AND "
            sql_strings += "vendor=computerspace "
        if (vdn == 'on'):
            if sql_strings.split()[-1] != 'WHERE':
                sql_strings += "AND "
            sql_strings += "vendor=vedantcomputers "
        if (prm == 'on'):
            if sql_strings.split()[-1] != 'WHERE':
                sql_strings += "AND "
            sql_strings += "vendor=primeabgb "
        if (itd == 'on'):
            if sql_strings.split()[-1] != 'WHERE':
                sql_strings += "AND "
            sql_strings += "vendor=itdepot "
    return render_template('index.html', sql=sql_strings)

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)
