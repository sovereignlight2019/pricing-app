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
    return render_template("vinyl.html")

@media_bp.route('/media/paper', methods=['GET'])
def paper():
    return render_template("paper.html")

@media_bp.route('/media/substrates', methods=['GET'])
def paper():
    return render_template("substrates.html")