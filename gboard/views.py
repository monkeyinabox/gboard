from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, login_user, current_user, logout_user

from gboard.infrastructure.forms import ServerForm, DomainForm
from gboard.infrastructure import Server, Domain, ResourceRecord
from .forms import LoginForm
from .models import User
from gboard import app, db

from pprint import pprint

import dns

@app.route('/domain', methods=['GET','POST'])
def domain():
    serverform = ServerForm()
    domainform = DomainForm()
    data = Domain.query.filter_by().all()
    domainform.master.query = Server.query.filter_by()
    
    
    if domainform.validate_on_submit():
        domain = Domain()
        domainform.populate_obj(domain)
        domain.master = domainform.master.data.id
        db.session.add(domain)
        db.session.commit()
        flash('A confirmation email has been sent via email.', 'success')

        domain.axfr()

        return redirect(url_for('index'))

    return render_template("domain.html",
            domainform=domainform,
            data=data)

@app.route('/rr', methods=['GET','POST'])
def rr():
    #data = ResourceRecord.query.filter_by().all()

    data = db.session.query(ResourceRecord).join(ResourceRecord.server).filter_by().all()
    return render_template("resource_record.html",
            data=data)



@app.route('/domain/query/<string:master>/<string:domain>')
def axfr():
    z = dns.zone.from_xfr(dns.query.xfr(domain.master.__str__(), domain.name))
    pprint(z)



@app.route('/', methods=['GET','POST'])
def index():
    serverform = ServerForm()
    domainform = DomainForm()
    data = Server.query.filter_by().all()

    if serverform.validate_on_submit():
        server = Server()
        serverform.populate_obj(server)

        db.session.add(server)
        db.session.commit()
        flash('A confirmation email has been sent via email.', 'success')

    return render_template("index.html",
            serverform=serverform,
            data=data)

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
