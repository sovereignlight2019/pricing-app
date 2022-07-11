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
    db = "dbname=sprocket user=sprocket password=Sprocket123 host=localhost"
    conn = psycopg2.connect(db)
    cur = conn.cursor()
    
    # display form
    cur.execute("""SELECT * FROM media;""")
    rows = cur.fetchall()
    conn.commit()
    cur.close
    conn.close()
    
    return render_template("vinylmedia.html",list=rows)

@media_bp.route('/media/paper', methods=['GET'])
def paper():
    db = "dbname=sprocket user=sprocket password=Sprocket123 host=localhost"
    conn = psycopg2.connect(db)
    cur = conn.cursor()
    
    # display form
    cur.execute("""SELECT * FROM media_stock where ;""")
    rows = cur.fetchall()
    conn.commit()
    cur.close
    conn.close()
    
    return render_template("papermedia.html",list=rows)


@media_bp.route('/media/vinyl/add', methods=['GET', 'POST'])
def vinyl_add():
    db = "dbname=sprocket user=sprocket password=Sprocket123 host=localhost"
    conn = psycopg2.connect(db)
    cur = conn.cursor()
    
    if request.method == 'GET':
        # display form
        cur.execute("""SELECT * FROM media;""")
        rows = cur.fetchall()
        cur.close
        conn.close()
        return render_template("vinylmedia.html",list=rows)

    else:
        # submit form

        vendor= request.form['inputVendor']
        product = request.form['inputProduct']
        supplier = request.form['inputSupplier']
        rollwidth = request.form['inputRollWidth']
        rolllength = request.form['inputRollLength']
        cost = request.form['inputCost']
        type = "vinyl"


        cur.execute("""INSERT into media(type,vendor,product,supplier,roll_width,roll_length,cost) VALUES (%s,%s,%s,%s,%s,%s,%s) RETURNING *;""", (type,vendor,product,supplier,rollwidth,rolllength,cost))
        rows = cur.fetchall()
        conn.commit()
        cur.close
        conn.close()

        return redirect("/media/vinyl")

@media_bp.route('/media/paper/add', methods=['GET', 'POST'])
def paper_add():
    db = "dbname=sprocket user=sprocket password=Sprocket123 host=localhost"
    conn = psycopg2.connect(db)
    cur = conn.cursor()
    
    if request.method == 'GET':
        # display form
        cur.execute("""SELECT * FROM media WHERE type = 'paper';""")
        rows = cur.fetchall()
        cur.close
        conn.close()
        return render_template("paper.html",list=rows)

    else:
        # submit form

        vendor= request.form['inputVendor']
        product = request.form['inputProduct']
        supplier = request.form['inputSupplier']
        papersize = request.form['inputPaperSize']
        paperweight = request.form['inputRollWeight']
        paperqty = request.form['inputPaperQTY']
        cost = request.form['inputCost']
        type = "paper"


        cur.execute("""INSERT into media(type,vendor,product,supplier,paper_size,paper_weight,paper_qty,cost) VALUES (%s,%s,%s,%s,%s,%s,%s,%s) RETURNING *;""", (type,vendor,product,supplier,papersize,paperweight,paperqty,cost))
        rows = cur.fetchall()
        conn.commit()
        cur.close
        conn.close()

        return redirect("/media/paper")

@media_bp.route('/media/vinyl/edit/<id>', methods=['GET', 'POST'])
def vinyl_edit(id):

    db = "dbname=sprocket user=sprocket password=Sprocket123 host=localhost"
    conn = psycopg2.connect(db)
    cur = conn.cursor()

    if request.method == 'GET':
        cur.execute("""SELECT * FROM media WHERE id = %s;""", (id))
        row = cur.fetchone()
        cur.close
        conn.close()
    
        return render_template("editvinyl.html", item=row)

    else:
        # Get Form data
        vendor= request.form['inputVendor']
        product = request.form['inputProduct']
        supplier = request.form['inputSupplier']
        rollwidth = request.form['inputRollWidth']
        rolllength = request.form['inputRollLength']
        cost = request.form['inputCost']
        type = "vinyl"

        # Update table row
        conn = psycopg2.connect(db)
        cur = conn.cursor()
        cur.execute(
           "UPDATE media SET vendor=%s, product=%s, supplier=%s, roll_width=%s, roll_length=%s, cost=%s"        
           " WHERE id=%s",
           (vendor,product,supplier,rollwidth,rolllength,cost,int(id),));
        updated_rows = cur.rowcount
        conn.commit()
        cur.close
        conn.close()

        return redirect("/media/vinyl")

@media_bp.route('/media/substrates', methods=['GET'])
def substrates():
    return render_template("substrates.html")