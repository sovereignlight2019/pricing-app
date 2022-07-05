from flask import Blueprint, render_template, request, redirect, url_for, session
from flask import current_app as app
import psycopg2


# Blueprint Configuration
assetcosts_bp = Blueprint(
    'assetcosts_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

@assetcosts_bp.route('/assets', methods=['GET', 'POST'])
def assets():
    if request.method == 'GET':
        dbName = "sprocket"
        db = "dbname=" + dbName + " user=sprocket password=Sprocket123 host=localhost"
        conn = psycopg2.connect(db)
        cur = conn.cursor()
        cur.execute("""SELECT * FROM running_costs;""")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        my_list = []
        for row in rows:
            my_list.append(row)
    return render_template("assetscosts.html", results=my_list)

@assetcosts_bp.route('/assets/addcost', methods=['GET', 'POST'])
def add_asset():
    if request.method == 'GET':
        # display form
        return render_template("addcost.html")

    else:
        # submit form
        # add details to DB and return to assets page
        return render_template("assetscosts.html")

