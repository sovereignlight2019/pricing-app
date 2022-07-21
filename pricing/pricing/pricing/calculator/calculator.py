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

@calculator_bp.route('/calculator/digitalprint', methods=['GET', 'POST'])
def calculator_digitalprint():
    db = "dbname=sprocket user=sprocket password=Sprocket123 host=localhost"
    conn = psycopg2.connect(db)
    cur = conn.cursor()

    if request.method == 'GET':
        # Display form
        cur.execute("""SELECT * FROM media where type = 'paper';""")
        media_rows = cur.fetchall()
        cur.execute("""SELECT * FROM asset_costs;""")
        asset_rows = cur.fetchall()
        cur.close
        conn.close()
        return render_template("digitalprint.html", media=media_rows,assets=asset_rows)

    else:
        # Get costing details
        impression_cost = 0.06
        
        # Get form info

        asset = request.form['jobAsset']
        job_media = int(request.form['media'])
        print_option = request.form['printRadios']
        if request.form['whiteInk']:
            white_ink = 1
        if request.form['glossInk']:
            gloss_ink = 1
        if request.form['silverInk']:
            silver_ink = 1
        if request.form['goldInk']:
            gold_ink = 1
        job_duration = int(request.form['jobDuration'])
        paper_size = int(request.form['paperSize'])
        print_size = int(request.form['finishSize'])
        if request.form['laminated']:
            laminated = 1
        if request.form['creased']:
            creased = 1
        if request.form['folded']:
            folded = 1
        if request.form['numbered']:
            numbered = 1
        quantity = int(request.form['jobQuantity'])
        setup_cost = float(request.form['setupCost'])

        # Get machine cost
        cur.execute("""SELECT monthly_depreciation FROM asset_costs where id=%s;""",(asset,))
        asset_cost = cur.fetchone()
        assetCost = (asset_cost[0] / 176) * (job_duration/60)

        # Get Media cost
        cur.execute("""SELECT paper_size,cost,product,cost/qty::float AS (sheet_cost) FROM media WHERE id = %s;""", (job_media,))
        media_details = cur.fetchone()

        # Get Prints per Page
        SRA2 = { 'SRA3': 2, 'A3': 2, 'A4:': 4, 'A5': 8, 'A6': 16, 'DL': 12}
        SRA3 = { 'A3': 1, 'A4': 2, 'A5': 4, 'A6': 8, 'DL': 6 }
        A4 = { 'A4': 1, 'A5': 2, 'A6': 4, 'DL': 3}
        if paper_size is 'SRA3':
            prints_per_page = SRA3[print_size]
        if paper_size is 'A3':
            prints_per_page = SRA3[print_size]
        if paper_size is 'A4':
            prints_per_page = A4[print_size]
        
        # Get number of impressions
        if print_option is 'simplex':
            number_impressions = quantity / prints_per_page * print_option
        else:
            number_impressions = 2 * quantity / prints_per_page

        # Get Paper Quantity
        number_sheets = media_details['paper_size'] / paper_size

        # Get Machine Costs


        jobCost = { 'impressions': number_impressions * impression_cost,
                     'paper_cost': number_sheets * media_details['sheet_cost'],
                     'printer_cost': assetCost
                }
        
        total_cost = sum(jobCost.values())
        return("Total Cost: £" + str(jobCost))
        cur.close
        conn.close()

@calculator_bp.route('/calculator/vinyl', methods=['GET', 'POST'])
def calculator_vinyl():
    db = "dbname=sprocket user=sprocket password=Sprocket123 host=localhost"
    conn = psycopg2.connect(db)
    cur = conn.cursor()

    if request.method == 'GET':
        # Display form
        cur.execute("""SELECT * FROM media where type = 'vinyl';""")
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
        # For job to fit in roll width / job width has to be greater than 1 
        if (roll_width / job_width) or (roll_width / job_height)>= 1:

            # width density - rounded DOWN to int
            # based on above if statement width density has to be at least 1
            # use int() to round down
            width_density = int(roll_width / job_width)
            # Check set the density to job quantity if it is greater.
            # eg - if density is 4 and qty is 2, then set density to qty
            if width_density > quantity:
                width_density = quantity
            
            # number of rows - rounded UP to nearest int
            # Number of rows is the quantity divided by the density
            # rounded up to the row
            number_rows = math.ceil(quantity / width_density)
            # padding
            # add the space between rows and columns
            vert_padding = number_rows * 25
            horiz_padding = (width_density -1) * 25

            # Calculate the required roll area 
            roll_area = ((number_rows * job_height) + vert_padding) * roll_width
            # Calculate job area
            job_area = ((number_rows * job_height) + vert_padding) * ((width_density * job_width) + horiz_padding)
            
            # width area density 
            density_width = job_area / roll_area

            # -----------------------------------

            # height density - rounded DOWN to int
            height_density = int(roll_width / job_height)
            
            # Check set the density to job quantity if it is greater.
            # eg - if density is 4 and qty is 2, then set density to qty
            if height_density > quantity:
                height_density = quantity
            
            # number of rows - rounded UP to nearest int
            # Number of rows is the quantity divided by the density
            # rounded up to the row
            number_rows = math.ceil(quantity / height_density)
            # padding
            # add the space between rows and columns
            vert_padding = (number_rows * 25)
            horiz_padding = (height_density -1) * 25

            # required roll area 
            roll_area = ((number_rows * job_width) + vert_padding) * roll_width
            # job area
            job_area = ((number_rows * job_width) + vert_padding) * ((height_density * job_height) + horiz_padding)
            
            # height area density 
            density_height = job_area / roll_area

            # Check best density
            # This is done by calculating the area ration between the different orientations
            # Take the media area needed  and divide by the area of the total job
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
            # Return Error
            return("ERROR JOB DOES NOT FIT")

        total_media_cost = (total_media_usage / 1000) * media_cost

        # Get Running Cost
        cur.execute("""SELECT SUM (cost) AS total FROM running_costs;""")
        run_cost = cur.fetchone()
        oh_cost = (run_cost[0] / 176) * (job_duration/60)

        # Get Machine Cost
        cur.execute("""SELECT monthly_depreciation FROM asset_costs where id=%s;""",(asset,))
        asset_cost = cur.fetchone()
        assetCost = (asset_cost[0] / 176) * (job_duration/60)

        total_cost = oh_cost + total_media_cost + assetCost + setup_cost

        cur.close
        conn.close()
        return render_template("vinyljob.html",assetcost=assetCost,totalcost=total_cost,setupcost=setup_cost,overhead_cost=oh_cost,density=highest_density,rows=number_rows,media_required=total_media_usage,cost=total_media_cost,width=job_width,height=job_height,product=product_name,qty=quantity,mediaCost=media_cost)