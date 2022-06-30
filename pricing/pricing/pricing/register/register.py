from flask import Flask, render_template, url_for, flash, redirect, Blueprint
from flask import current_app as app



# Blueprint Configuration
register_bp = Blueprint(
    'register_bp', __name__,
    template_folder='templates',
    static_folder='static'
)
