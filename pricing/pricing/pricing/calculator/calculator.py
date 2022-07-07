from flask import Blueprint, render_template, request, redirect, url_for, session
from flask import current_app as app
from configparser import ConfigParser
import psycopg2, string, os, math, random


# Blueprint Configuration
calculator_bp = Blueprint(
    'calculator_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

@calculator_bp.route('/calculator/uvprint', methods=['GET'])
def calculator_uvprint():

    if request.method == 'GET':
        # Display form
        db = "dbname=sprocket user=sprocket password=Sprocket123 host=localhost"
        conn = psycopg2.connect(db)
        cur = conn.cursor()

        cur.execute("""SELECT * FROM media;""")
        media_rows = cur.fetchall()
        cur.execute("""SELECT * FROM asset_costs;""")
        asset_rows = cur.fetchall()
        cur.close
        conn.close()
        return render_template("uvprint.html", media=media_rows,assets=asset_rows)

@calculator_bp.route('/calculator/vinyl', methods=['GET'])
def calculator_vinyl():

    if request.method == 'GET':
        # Display form
        db = "dbname=sprocket user=sprocket password=Sprocket123 host=localhost"
        conn = psycopg2.connect(db)
        cur = conn.cursor()

        cur.execute("""SELECT * FROM media;""")
        media_rows = cur.fetchall()
        cur.execute("""SELECT * FROM asset_costs;""")
        asset_rows = cur.fetchall()
        cur.close
        conn.close()
        return render_template("vinyl.html", media=media_rows,assets=asset_rows)
    
    else:
        # Get form info

        return render_template("vinyljob.html")