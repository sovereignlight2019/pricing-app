from flask import Blueprint, render_template, request, redirect, url_for, session
from flask import current_app as app


# Blueprint Configuration
assetcosts_bp = Blueprint(
    'assetcosts_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

@register_bp.route('/assets', methods=['GET'])
def assets():
    return render_template("assetcosts.html")