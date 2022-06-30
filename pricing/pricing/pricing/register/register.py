from flask import Blueprint, render_template, request, redirect, url_for, session
from flask import current_app as app
from form import RegistrationForm


# Blueprint Configuration
register_bp = Blueprint(
    'register_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

@register_bp.route('/register', methods=['GET'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User(form.username.data, form.email.data,
                    form.password.data)
        #db_session.add(user)      Adds user to database
        flash('Thanks for registering')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)