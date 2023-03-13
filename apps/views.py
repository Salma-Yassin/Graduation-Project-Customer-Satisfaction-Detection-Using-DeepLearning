# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

# Flask modules
from flask   import render_template, request, flash, redirect, url_for, jsonify
from jinja2  import TemplateNotFound
from .models import User
from flask_login import login_user, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import db 
from random import sample 
from .inference import query
import sys

# App modules
from apps import app

@app.route('/data')
def get_chart_data():
   # generating random data for testing 
   return jsonify({'series':sample(range(1,100),7)})

@app.route('/media_data')
def get_media_data():
   # generating random data for testing 
   return jsonify({'data':[{'URL':'https://www.youtube.com/watch?v=poZt1f43gBc','Type':'vedio','Location':'Maady','EmployeeID' : '20147501'},{'URL':'https://www.youtube.com/watch?v=qDc484XBFjI','Type':'vedio','Location':'October','EmployeeID' : '201871501'}]})


# Pages -- Dashboard
# @app.route('/', defaults={'path': 'dashboard.html'})
@app.route('/', methods=['GET', 'POST'])
@login_required
def pages_dashboard():
  if request.method == 'POST':
     # retrive fields from data base 
     url = request.form.get('url')
     category = query(url)        

     # add record to database 
     #show data 
     #return redirect(url_for('pages_history'))
     return render_template('pages/dashboard/history.html', segment='history', parent='pages', user=current_user, resulto= category)
  return render_template('pages/dashboard/dashboard.html', segment='dashboard', parent='pages', user=current_user)


# Pages

@app.route('/pages/history/')
@login_required
def pages_history():
  return render_template('pages/dashboard/history.html', segment='history', parent='pages', user=current_user)

@app.route('/pages/settings/')
@login_required
def pages_settings():
  return render_template('pages/settings.html', segment='settings', parent='pages',user=current_user)

@app.route('/pages/upgrade-to-pro/')
def pages_upgrade_to_pro():
  return render_template('pages/upgrade-to-pro.html', segment='upgrade_to_pro', parent='pages')

# Pages -- Tables

@app.route('/pages/tables/bootstrap-tables/')
@login_required
def pages_tables_bootstrap_tables():
  return render_template('pages/tables/bootstrap-tables.html', segment='bootstrap_tables', parent='tables', user=current_user)

# Pages -- Pages examples

@app.route('/pages/examples/404/')
def pages_examples_404():
  return render_template('pages/examples/404.html', segment='404', parent='pages')

@app.route('/pages/examples/500/')
def pages_examples_500():
  return render_template('pages/examples/500.html', segment='500', parent='pages')

# Accounts

@app.route('/accounts/sign-in/', methods=['GET', 'POST'])
def accounts_sign_in():
  if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfuly!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('pages_dashboard'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')
  #return render_template("sign-in.html", user=current_user)
  return render_template('accounts/sign-in.html', segment='sign_in', parent='accounts')

@app.route('/accounts/sign-up/', methods=['GET', 'POST'])
def accounts_sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        #return render_template('pages/dashboard/dashboard.html', segment='dashboard', parent='pages')

        user = User.query.filter_by(email= email).first()
        if user:
            flash('Email already exists.', category='error')
            #return render_template('pages/dashboard/dashboard.html', segment='dashboard', parent='pages')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
            #return render_template('pages/dashboard/dashboard.html', segment='dashboard', parent='pages')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
            #return render_template('pages/dashboard/dashboard.html', segment='dashboard', parent='pages')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
            #return render_template('pages/dashboard/dashboard.html', segment='dashboard', parent='pages')
        else:
            new_user = User(email=email, password= generate_password_hash(password1, method='sha256')) 
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            # return render_template('pages/dashboard/dashboard.html', segment='dashboard', parent='pages')
            return redirect(url_for('pages_dashboard'))

    # return render_template("sign_up.html", user=current_user) 
    return render_template('accounts/sign-up.html', segment='sign_up', parent='accounts')


@app.route('/accounts/forgot-password/')
def accounts_forgot_password():
  return render_template('accounts/forgot-password.html', segment='forgot_password', parent='accounts')

@app.route('/accounts/reset-password/')
def accounts_reset_password():
  return render_template('accounts/reset-password.html', segment='reset_password', parent='accounts')

@app.route('/accounts/lock/')
def accounts_lock():
  return render_template('accounts/lock.html', segment='lock', parent='accounts')

@app.route('/accounts/password-change/')
def accounts_password_change():
  return render_template('accounts/password-change.html', segment='password-change', parent='accounts')

@app.route('/accounts/logout/')
@login_required # makes sure that the user is logged out only if they are logged in
def logout():
    logout_user()
    return redirect(url_for('accounts_sign_in'))

# Pages Components

@app.route('/pages/components/buttons/')
def pages_components_buttons():
  return render_template('pages/components/buttons.html', segment='buttons', parent='components')

@app.route('/pages/components/notifications/')
def pages_components_notifications():
  return render_template('pages/components/notifications.html', segment='notifications', parent='components')

@app.route('/pages/components/forms/')
def pages_components_forms():
  return render_template('pages/components/forms.html', segment='forms', parent='components')

@app.route('/pages/components/modals/')
def pages_components_modals():
  return render_template('pages/components/modals.html', segment='modals', parent='components')

@app.route('/pages/components/typography/')
def pages_components_typography():
  return render_template('pages/components/typography.html', segment='typography', parent='components')