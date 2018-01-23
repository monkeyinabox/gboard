from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, login_user, current_user, logout_user

from .forms import LoginForm
from .models import User
from . import app

from scapy.all import *
import graphviz

def update_map():
    res,unans = traceroute(["www.microsoft.com","www.cisco.com","www.yahoo.com","www.wanadoo.fr","www.pacsec.com"],dport=[80,443],maxttl=20,retry=-2)
    res.graph()
    res.graph(type="ps",target="| lp")
    res.graph(target="> static/images/graph.svg")

@app.route('/', methods=['GET','POST'])
def index():
    update_map()
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

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404