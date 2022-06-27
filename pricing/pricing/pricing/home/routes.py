from flask import Blueprint
from flask import current_app as app


# Blueprint Configuration
home_bp = Blueprint(
    'home_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

def generateMetrics():
    return "hello world"

@home_bp.route('/', methods=['GET'])
def home():
    response = make_response(generateMetrics(), 200)
    response.mimetype = "text/plain"
    return response