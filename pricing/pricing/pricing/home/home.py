from flask import Blueprint
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
def home():
    return render_template('pricing-login.html')

@home_bp.route('/logout', methods=['GET'])
def home():
    return "Logout"