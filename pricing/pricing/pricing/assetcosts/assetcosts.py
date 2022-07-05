rom flask import Blueprint, render_template, request, redirect, url_for, session
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
    if request.method == 'GET':
       # Display form
    
       db = "dbname=sprocket user=sprocket password=Sprocket123 host=localhost"
       conn = psycopg2.connect(db)
       cur = conn.cursor()
       cur.execute("""SELECT * FROM asset_costs where id = %s;""", (asset_id))
       asset_rows = cur.fetchall()
       cur.close
       conn.close()
       return render_template("editasset.html", assets=asset_rows)

    else:
       # submit form
       db = "dbname=sprocket user=sprocket password=Sprocket123 host=localhost"
       conn = psycopg2.connect(db)
       cur = conn.cursor()

       # update data

       cur.execute("""SELECT SUM (cost) AS total FROM running_costs;""")
       cost = cur.fetchall()
       cur.execute("""SELECT * FROM running_costs;""")
       rows = cur.fetchall()
       cur.execute("""SELECT * FROM asset_costs;""")
       asset_rows = cur.fetchall()

       cur.close
       conn.close()

       for row in cost:
            monthly_cost.append(row[0])

       return render_template("assetscosts.html", results=my_list, cost=monthly_cost, assets=asset_rows)