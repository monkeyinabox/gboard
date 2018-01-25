from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, login_user, current_user, logout_user

from .forms import LoginForm
from .models import User
from . import app

@app.route('/', methods=['GET','POST'])
def index():
    return render_template("index.html")

@app.route('/login', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()

    if form.validate_on_submit():
        user, authenticated = User.authenticate(form.email.data,
                                    form.password.data)

        if user and authenticated:
            remember = request.form.get('remember') == 'y'
            if login_user(user, remember=remember):
                flash("You are now lgged ins", 'success')
            return redirect(url_for('index'))
        else:
            flash('Sorry, invalid login', 'danger')

    return render_template('user/login.html', form=form)
