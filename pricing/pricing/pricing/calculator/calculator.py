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

@calculator_bp.route('/calculator/vinyl', methods=['GET', 'POST'])
def calculator_vinyl():
    db = "dbname=sprocket user=sprocket password=Sprocket123 host=localhost"
    conn = psycopg2.connect(db)
    cur = conn.cursor()

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

        asset = request.form['jobAsset']
        job_width = int(request.form['jobWidth'])
        job_height = int(request.form['jobHeight'])
        job_duration = int(request.form['jobDuration'])
        job_media = request.form['jobMedia']
        quantity = int(request.form['jobQuantity'])

        cur.execute("""SELECT roll_width,cost FROM media WHERE id = %s RETURNING *;""", (job_media,))
        media_details = cur.fetchone()
        cur.close
        conn.close()

        roll_width = media_details[0]
        media_cost = media_details[1]

        # Use Job Width to determine job density
        width_density = int(roll_width / job_width)
        height_density = int(roll_width / job_height)

        # Check best density
        density = {'height': int(roll_width / job_height), 'width': int(roll_width / job_width)}
        highest_density = max(density, key=density.get)

        if highest_density is 'width':
            media_length = job_height
            number_rows = quantity / int(roll_width / job_width)
            total_media_usage = math.ceil(job_height * number_rows * 1.1)


        else:
            media_length = job_width
            number_of_rows = quantity / int(roll_width / job_height)
            total_media_usage = math.ceil(job_width * number_rows * 1.1)

        total_media_cost = (total_media_usage / 1000) * media_cost

        

        # Get Media Width and Calculate Job Density


        return render_template("vinyljob.html")