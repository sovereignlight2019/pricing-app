from operator import truediv
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
        setup_cost = float(request.form['setupCost'])

        cur.execute("""SELECT roll_width,cost,product FROM media WHERE id = %s;""", (job_media,))
        media_details = cur.fetchone()


        # Subtract 25mm from each side
        roll_width = media_details[0] - 50
        media_cost = media_details[1]
        product_name = media_details[2]
        padding = 25

        # Check if job will fit on Media Width
        if (roll_width / job_width) >= 1:

            # width density - rounded DOWN to int
            width_density = int(roll_width / job_width)
            if width_density > quantity:
                width_density = quantity
            
            # number of rows - rounded UP to nearest int
            number_rows = math.ceil(quantity / width_density)
            # padding
            vert_padding = number_rows * 25
            horiz_padding = (width_density -1) * 25
            # required roll area 
            roll_area = ((number_rows * job_height) + vert_padding) * roll_width
            # job area
            job_area = ((number_rows * job_height) + vert_padding) * ((width_density * job_width) + horiz_padding)
            # width area density 
            density_width = job_area / roll_area

            # height density - rounded DOWN to int
            height_density = int(roll_width / job_height)
            if height_density > quantity:
                height_density = quantity
            # number of rows - rounded UP to nearest int
            number_rows = math.ceil(quantity /height_density)
            # padding
            vert_padding = (number_rows * 25)
            horiz_padding = (height_density -1) * 25
            # required roll area 
            roll_area = ((number_rows * job_width) + vert_padding) * roll_width
            # job area
            job_area = ((number_rows * job_width) + vert_padding) * ((height_density * job_height) + horiz_padding)
            # height area density 
            density_height = job_area / roll_area

            # Check best density

            density = {'height': density_height, 'width': density_width}
            highest_density = max(density, key=density.get)

            if highest_density is 'width':
                number_rows = math.ceil(quantity / int(roll_width / job_width))
                excess = number_rows * 50
                total_media_usage = (job_height * number_rows) + excess

            else:

                number_rows = math.ceil(quantity / int(roll_width / job_height))
                excess = number_rows * 50
                total_media_usage = (job_width * number_rows) + excess

        else:
            # Job does not fit horizontally
            number_rows = quantity / int(roll_width / job_height)
            excess = number_rows * 25 + 25
            total_media_usage = (job_width * number_rows) + excess

        total_media_cost = (total_media_usage / 1000) * media_cost

        # Get Running Cost
        cur.execute("""SELECT SUM (cost) AS total FROM running_costs;""")
        run_cost = cur.fetchone()
        oh_cost = (run_cost[0] / 176) * (job_duration/60)

        # Get Machine Cost
        cur.execute("""SELECT monthly_depreciation FROM asset_costs where id=%s;""",(asset,))
        asset_cost = cur.fetchone()
        assetCost = (asset_cost / 176) * (job_duration/60)

        total_cost = oh_cost + total_media_cost + setup_cost + assetCost

        cur.close
        conn.close()
        return render_template("vinyljob.html",assetcost=assetCost,totalcost=total_cost,setupcost=setup_cost,overhead_cost=oh_cost,density=highest_density,rows=number_rows,media_required=total_media_usage,cost=total_media_cost,width=job_width,height=job_height,product=product_name, qty=quantity,mediaCost=media_cost)