from flask import Blueprint, render_template, request, redirect, url_for, session
from flask import current_app as app


# Blueprint Configuration
home_bp = Blueprint(
    'home_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

@home_bp.route('/', methods=['GET'])
def home():
    return "Dashboard"

@home_bp.route('/login', methods=['GET'])
def login():
    return render_template('pricing-login.html')

@home_bp.route('/logout', methods=['GET'])
def logout():
    return "Logout"

