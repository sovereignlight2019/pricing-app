from flask import Blueprint, render_template, request, redirect, url_for, session
from flask import current_app as app
from configparser import ConfigParser
import psycopg2, string, os, math, random


# Blueprint Configuration
media_bp = Blueprint(
    'media_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

@media_bp.route('/media', methods=['GET'])
def media():
    return render_template("media.html")

@media_bp.route('/media/vinyl', methods=['GET'])
def vinyl():
    return render_template("vinyl.html")

@media_bp.route('/media/vinyl/add', methods=['GET', 'POST'])
def vinyl_add():
    db = "dbname=sprocket user=sprocket password=Sprocket123 host=localhost"
    conn = psycopg2.connect(db)
    cur = conn.cursor()
    
    if request.method == 'GET':
        # display form
        cur.execute("""SELECT * FROM running_costs;""")
        rows = cur.fetchall()
        return render_template("vinyl.html",list=rows)

    else:
        # submit form

        vendor= request.form['inputVendor']
        product = request.form['inputVendor']
        supplier = request.form['inputSupplier']
        rollwidth = request.form['inputRollWidth']
        rolllength = request.form['inputRollLength']
        cost = request.form['inputCost']


        cur.execute("""INSERT into media(vendor,product,supplier,roll_width,roll_length,cost) VALUES (%s,%s,%s,%s,%s,%s) RETURNING *;""", (vendor,product,supplier,rollwidth,rolllength,cost)
        rows = cur.fetchall()
        conn.commit()
        cur.close
        conn.close()

        return render_template("vinyl.html")

@media_bp.route('/media/paper', methods=['GET'])
def paper():
    return render_template("paper.html")

@media_bp.route('/media/substrates', methods=['GET'])
def substrates():
    return render_template("substrates.html")