from flask import Flask, render_template, url_for, flash, redirect, Blueprint, session
from flask import current_app as app
from forms import RegistrationForm


# Blueprint Configuration
home_bp = Blueprint(
    'home_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

@home_bp.route('/', methods=['GET'])
def home():
    return "Dashboard"

@register_bp.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

@home_bp.route('/login', methods=['GET'])
def login():
    return render_template('pricing-login.html')

@home_bp.route('/logout', methods=['GET'])
def logout():
    return "Logout"

