from flask import Blueprint, render_template, request, redirect, url_for, session
from flask import current_app as app


# Blueprint Configuration
register_bp = Blueprint(
    'register_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

@register_bp.route("/register", methods=['GET', 'POST'])
    def register():
        form = RegistrationForm()
        #if form.validate_on_submit():
            #flash(f'Account created for {form.username.data}!', 'success')
            #return redirect(url_for('home'))
        return render_template('register.html', title='Register', form=form)
