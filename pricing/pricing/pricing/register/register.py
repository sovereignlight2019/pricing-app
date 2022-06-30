from flask import Blueprint, render_template, request, redirect, url_for, session
from flask import current_app as app


# Blueprint Configuration
register_bp = Blueprint(
    'register_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

@register_bp.route('/register', methods=['GET'])
def register():
    return "Registration Page"  