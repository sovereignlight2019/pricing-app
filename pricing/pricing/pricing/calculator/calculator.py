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

@calculator_bp.route('/calculator', methods=['GET'])
def calculator():
    return render_template("calculator.html")