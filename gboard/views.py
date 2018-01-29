from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, login_user, current_user, logout_user

from gboard.infrastructure.forms import ServerForm, DomainForm, DomainSelectForm
from gboard.infrastructure import Server, Domain, ResourceRecord
from .forms import LoginForm
from .models import User
from gboard import app, db

from pprint import pprint

import dns


@app.route('/compare', methods=['GET','POST'])
def compare():
    form = DomainSelectForm()
    form.left_domain.query = Domain.query.filter_by()
    form.right_domain.query = Domain.query.filter_by()

    if form.validate_on_submit():
        left_domain = Domain.query.get(form.left_domain.data.id)
        right_domain = Domain.query.get(form.right_domain.data.id)

        left_soa = ResourceRecord.query.filter_by(rr_type='SOA', domain_id=left_domain.id).first().data
        right_soa = ResourceRecord.query.filter_by(rr_type='SOA', domain_id=right_domain.id).first().data
        
        return render_template("compare.html",
            form=form,
            left_id=left_domain.id, 
            right_id=right_domain.id,
            left_soa=left_soa,
            right_soa=right_soa)

    return render_template("compare.html",
            form=form)


@app.route('/domain', methods=['GET','POST'])
def domain():
    serverform = ServerForm()
    domainform = DomainForm()
    data = Domain.query.filter_by().all()
    domainform.master.query = Server.query.filter_by()
    domain_id=1
    
    if domainform.validate_on_submit():
        domain = Domain()
        domainform.populate_obj(domain)
        domain.master = domainform.master.data.id
        db.session.add(domain)
        db.session.commit()
        flash('A confirmation email has been sent via email.', 'success')

        # domain.axfr()
        
        return redirect(url_for('index'))

    return render_template("domain.html",
            domainform=domainform,
            data=data,
            domain_id=domain_id)

@app.route('/rr', methods=['GET','POST'])
def rr():
    #data = ResourceRecord.query.filter_by().all()

    data = db.session.query(ResourceRecord).join(ResourceRecord.server).filter_by().all()
    return render_template("resource_record.html",
            data=data)

@app.route('/domain/axfr/<int:domain_id>', methods=['GET' ,'POST'])
def axfr(domain_id):
    domain = Domain.query.get(domain_id)
    domain.axfr()
    return redirect(url_for('rr'))

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
