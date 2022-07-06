from flask import Blueprint, render_template, request, redirect, url_for, session
from flask import current_app as app
import psycopg2, string, os, math, random


# Blueprint Configuration
assetcosts_bp = Blueprint(
    'assetcosts_bp', __name__,
    template_folder='templates',
    static_folder='static'
)



@assetcosts_bp.route('/assets', methods=['GET', 'POST'])
def assets():
    if request.method == 'GET':
        monthly_cost = []
        my_list = []
        asset_list = []
        dbName = "sprocket"
        db = "dbname=" + dbName + " user=sprocket password=Sprocket123 host=localhost"
        conn = psycopg2.connect(db)
        cur = conn.cursor()
        cur.execute("""SELECT * FROM running_costs;""")
        rows = cur.fetchall()
        cur.execute("""SELECT SUM (cost) AS total FROM running_costs;""")
        cost = cur.fetchall()
        cur.execute("""SELECT * FROM asset_costs;""")
        asset_rows = cur.fetchall()
        conn.close()
        for row in cost:
            monthly_cost.append(row[0])
        cur.close()
        conn.close()
        for row in rows:
            my_list.append(row)
    return render_template("assetscosts.html", results=my_list, cost=monthly_cost, assets=asset_rows)

@assetcosts_bp.route('/assets/addcost', methods=['GET', 'POST'])
def add_cost():
    if request.method == 'GET':
        # display form
        return render_template("addcost.html")

    else:
        # submit form
        # add details to DB and return to assets page
        monthly_cost = []
        my_list = []
        asset_list = []

        itemName = request.form['inputCostItem']
        itemVendor = request.form['inputVendor']
        itemFrequency = request.form['inputFrequency']
        itemCost = request.form['inputCost']

        db = "dbname=sprocket user=sprocket password=Sprocket123 host=localhost"
        conn = psycopg2.connect(db)
        cur = conn.cursor()
        cur.execute("""INSERT into running_costs(item,description,supplier,pmt_frequency,cost) VALUES (%s,%s,%s,%s,%s) RETURNING *;""", (itemName,itemName,itemVendor,itemFrequency,itemCost))
        rows = cur.fetchall()
        cur.execute("""SELECT SUM (cost) AS total FROM running_costs;""")
        cost = cur.fetchall()
        cur.execute("""SELECT * FROM running_costs;""")
        rows = cur.fetchall()
        cur.execute("""SELECT * FROM asset_costs;""")
        asset_rows = cur.fetchall()
        conn.commit()
        cur.close
        conn.close()
        for row in cost:
            monthly_cost.append(row[0])
        for row in rows:
            my_list.append(row)

        return render_template("assetscosts.html", results=my_list, cost=monthly_cost, assets=asset_rows)

@assetcosts_bp.route('/assets/addasset', methods=['GET', 'POST'])
def add_asset():
    if request.method == 'GET':
        # display form
        return render_template("addasset.html")

    else:
        # submit form
        # add details to DB and return to assets page
        monthly_cost = []
        my_list = []

        assetDesc = request.form['inputAssetDesc']
        assetMake = request.form['inputAssetMake']
        assetModel = request.form['inputAssetModel']
        assetCost = request.form['inputAssetCost']
        assetMonths = request.form['inputAssetMonths']
        monthlyDepreciation = float(assetCost) / int(assetMonths)

        db = "dbname=sprocket user=sprocket password=Sprocket123 host=localhost"
        conn = psycopg2.connect(db)
        cur = conn.cursor()
        cur.execute("""INSERT into asset_costs (item,make,model,cost,depreciation_months,monthly_depreciation) VALUES (%s,%s,%s,%s,%s,%s) RETURNING *;""", (assetDesc,assetMake,assetModel,assetCost,assetMonths,monthlyDepreciation))
        rows = cur.fetchall()
        cur.execute("""SELECT SUM (cost) AS total FROM running_costs;""")
        cost = cur.fetchall()
        cur.execute("""SELECT * FROM running_costs;""")
        rows = cur.fetchall()
        cur.execute("""SELECT * FROM asset_costs;""")
        asset_rows = cur.fetchall()
        conn.commit()
        cur.close
        conn.close()
        for row in cost:
            monthly_cost.append(row[0])
        for row in rows:
            my_list.append(row)

        return render_template("assetscosts.html", results=my_list, cost=monthly_cost, assets=asset_rows)

@assetcosts_bp.route('/assets/editasset/<asset_id>', methods=['GET', 'POST'])
def edit_asset(asset_id):

    # This section determines that it is a request to UPDATE the asset
    # It will return the form with populated values, based on a search from the <assed_id>
    #

    if request.method == 'GET':
       # Display form
       db = "dbname=sprocket user=sprocket password=Sprocket123 host=localhost"
       conn = psycopg2.connect(db)
       cur = conn.cursor()

       cur.execute("""SELECT * FROM asset_costs WHERE id = %s;""", (asset_id))
       asset_row = cur.fetchone()
       cur.close
       conn.close()
       return render_template("editasset.html", assets=asset_row)

    else:

    # This section is processed when the form is submitted (POST)
    # It gets the values from the form and updates the data base
    # It then also does a couple of searches for cossts and assets
    # and sends the data to the main asset/costs dashboard template

       # form submitted
       # Connect to DB
       db = "dbname=sprocket user=sprocket password=Sprocket123 host=localhost"
       conn = psycopg2.connect(db)
       cur = conn.cursor()

       # update data

       monthly_cost = []

       # Get Form Data
       assetDesc = request.form['inputAssetDesc']
       assetMake = request.form['inputAssetMake']
       assetModel = request.form['inputAssetModel']
       assetCost = request.form['inputAssetCost']
       assetMonths = request.form['inputAssetMonths']

       # Manipulate the depreciation cost
       monthlyDepreciation = float(assetCost) / int(assetMonths)

       # Update the row in the DB
       cur.execute("""UPDATE asset_costs set item=%s,make=%s,model=%s,cost=%s,depreciation_months=%s,monthly_depreciation=%s WHERE id=%s RETURNING *;""", (assetDesc,assetMake,assetModel,assetCost,assetMonths,monthlyDepreciation,asset_id))
       conn.commit

       cur.close
       conn.close()

    return redirect(url_for('assets'))

@assetcosts_bp.route('/assets/editcost/<cost_id>', methods=['GET', 'POST'])
def edit_cost(cost_id):

    # This section determines that it is a request to UPDATE the cost
    # It will return the form with populated values, based on a search from the <cost_id>
    #

    if request.method == 'GET':
       # Display form
       db = "dbname=sprocket user=sprocket password=Sprocket123 host=localhost"
       conn = psycopg2.connect(db)
       cur = conn.cursor()

       cur.execute("""SELECT * FROM running_costs WHERE id = %s;""", (cost_id))
       asset_row = cur.fetchone()
       cur.close
       conn.close()
       return render_template("editcost.html", results=asset_row)

    else:

    # This section is processed when the form is submitted (POST)
    # It gets the values from the form and updates the data base
    # It then also does a couple of searches for costs and assets
    # and sends the data to the main asset/costs dashboard template



       # update data

       monthly_cost = []

       # Get Form Data
       itemName = request.form['inputCostItem']
       itemVendor = request.form['inputVendor']
       itemFrequency = request.form['inputFrequency']
       itemCost = request.form['inputCost']

       # Update the row in the DB
       cur.execute("""UPDATE running_costs SET item=%s,description=%s,supplier=%s,pmt_frequency=%s,cost=%s WHERE id=%s RETURNING *;""", (itemName,itemName,itemVendor,itemFrequency,itemCost,cost_id))
       conn.commit
       cur.close
       conn.close()

       return redirect(url_for('assets'))