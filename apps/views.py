# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

# Flask modules
from flask   import Flask, render_template, request, flash, redirect, url_for, jsonify
import json
from jinja2  import TemplateNotFound
from .models import *
from flask_login import login_user, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import os
from wtforms.validators import InputRequired
from .models import db 
from random import sample 
from .inference import query,queryLocal
import sys
from .controller import controller

# App modules
from apps import app
# 
#
@app.route('/data') # this is a dummy api that should be removed 
def get_chart_data():
   # generating random data for testing 
   f = open("apps\Media_data.json")
   return json.load(f)

@app.route('/location_data')
def get_location_data():
   locations_table = UserLocations.query.filter_by(user_id= current_user.id).all()
   return jsonify(locations_table)

@app.route('/empolyee_data')
def get_empolyee_data():
   empolyee_table = UserMembers.query.filter_by(user_id= current_user.id).all()
   return jsonify(empolyee_table)

@app.route('/media_data')
def get_media_data():
   # generating random data for testing 
   #cursor= db.cursor()
   #history_table = cursor.execute("SELECT * FROM Media WHERE user_id=?;", [current_user.id])
   history_table = Media.query.filter_by(user_id= current_user.id).all()
   return jsonify(history_table)
   #return jsonify({'data':[{'URL':'https://www.youtube.com/watch?v=poZt1f43gBc','Type':'vedio','Location':'Maady','EmployeeID' : '20147501'},{'URL':'https://www.youtube.com/watch?v=qDc484XBFjI','Type':'vedio','Location':'October','EmployeeID' : '201871501'},{'URL':'https://www.youtube.com/watch?v=qDc484XBFjI','Type':'vedio','Location':'October','EmployeeID' : '201871501'},{'URL':'https://www.youtube.com/watch?v=qDc484XBFjI','Type':'vedio','Location':'October','EmployeeID' : '201871501'},{'URL':'https://www.youtube.com/watch?v=qDc484XBFjI','Type':'vedio','Location':'October','EmployeeID' : '201871501'}]})


# Pages -- Dashboard
# @app.route('/', defaults={'path': 'dashboard.html'})
def add_media_function(request):
  # retrive fields from data base
  urlink = request.form.get('url')
  media_type = request.form.get('media_type')
  emp_id = request.form.get('employee_id')
  location_add = request.form.get('location')
  media_name=request.form.get('media_name')
  user_id = current_user.id
  #file=request.files['file']

  if media_type == 'audio':
    file=request.files.get('file')
    if file: 
      filename = secure_filename(file.filename)
      file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'], filename)
      file.save(file_path)
      url=file_path
      category=queryLocal(url)
      flash('File has been uploaded.')
      detailed_results = json.dumps(category)
      results = (category)[0]['label']
      
      
    elif urlink:
      url=urlink
      category = query(urlink)
    # Convert dictionary to string
      detailed_results = json.dumps(category)
      results = (category)[0]['label']

  elif media_type == 'video':
    category = query(url)
    # Convert dictionary to string
    detailed_results = json.dumps(category)
    results = (category)[0]['label']
    #category = query_face(url)
    #category = 'Unknown'
    # call body model ---> 
  else:
   category = 'Unknown'

  
  controller.addMedia(media_name=media_name, url = url , type = media_type, user_id = user_id, location_address = location_add, member_id = emp_id, results = results, detailed_results= detailed_results)
  #created_media = Media.query.filter_by(url=url).first()
     #controller.addAnalysisResult(media_id= created_media.id, result=category[0]['label'])    
     #show data 
     #return redirect(url_for('pages_history'))

  

@app.route('/', methods=['GET', 'POST'])
@login_required
def pages_dashboard():
  if request.method == 'POST':
     add_media_function(request)
     return redirect(url_for('pages_history'))
  return render_template('pages/dashboard/dashboard.html', segment='dashboard', parent='pages', user=current_user)


# Pages

@app.route('/pages/history/', methods=['GET', 'POST'])
@login_required
def pages_history():
  if request.method == 'POST':
     add_media_function(request)
     return render_template('pages/dashboard/history.html', segment='history', parent='pages', user=current_user)
  return render_template('pages/dashboard/history.html', segment='history', parent='pages', user=current_user)

@app.route('/pages/manage/', methods=['GET', 'POST'])
@login_required
def pages_manage():
  if request.method == 'POST':
     user_id = current_user.id
     if request.form.get('Location_form'):       
        location = request.form.get('location')
        controller.addUserLocation(name=location, user_id=user_id)

     elif request.form.get('Employee_form'):
        empo_name = request.form.get('name')
        empo_gender = request.form.get('gender')
        empo_id = request.form.get('id')
        empo_location = request.form.get('location')
        controller.addUserMember(name=empo_name, user_id=user_id , member_id=empo_id, member_gender=empo_gender, location_id=empo_location)
        
  return render_template('pages/dashboard/manage.html', segment='manage', parent='pages',user=current_user)

##ِAdding About Us Page###
@app.route('/about')
def about():
    return render_template('about.html')

##########FEEDBACK & ContactUs PAGE ADDED NEWLY ####################

# ...

        # Save feedback to JSON file
'''        try:
            with open('apps/feedbacks.json', 'a') as f:
                data = {
                    'name': name,
                    'email': email,
                    'message': message
                }
                json.dump(data, f)
                f.write('\n')
        except Exception as e:
            flash(f'Error occurred while saving feedback: {str(e)}', category='error')'''
    

@app.route('/feedback_form', methods=['GET', 'POST'])
def feedback_form():
    if request.method == 'POST':
        
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        controller.AddFeedback(name=name, email=email, message=message)
        flash('Feedback Received!', category='success')

    return render_template('pages/dashboard/dashboard.html', segment='dashboard', parent='pages', user=current_user)


          #########
@app.route('/contact_form', methods=['GET', 'POST'])
def contact_form():
    if request.method == 'POST':
       
        email = request.form.get('email')
        message = request.form.get('message')
        controller.AddContact(email=email , message=message)
        flash('We will get back to you soon!', category='success')
  
    return render_template('pages/dashboard/dashboard.html', segment='dashboard', parent='pages', user=current_user)

####################END OF FEEDBACK & ContactUs ADDED NEWLY##################3

################Start of Statistics################
#Adding the top locations with satisfied results
@app.route('/satisfied_locations')
def satisfied_locations():
    satisfied_results = (
        Media.query
        .filter_by(results='hap')
        .group_by(Media.location_address)
        .with_entities(Media.location_address, func.count().label('count'))
        .order_by(func.count().desc())
        #.limit(5)to get top 5 locations
        .all()
    )

    # Separate the location addresses and counts into separate lists
    top_locations = [result.location_address for result in satisfied_results]
    counts = [result.count for result in satisfied_results]

    data = {'top_locations': top_locations, 'counts': counts}
    return json.dumps(data)



@app.route('/satisfied_employees')
def satisfied_employees():
    satisfied_results = (
        db.session.query(UserMembers.name, func.count())
        .join(Media, Media.member_id == UserMembers.member_id)
        .filter(Media.results == 'hap')
        .group_by(UserMembers.name)
        .order_by(func.count().desc())
        .all()
    )

    # Separate the member names and counts into separate lists
    top_members = [result[0] for result in satisfied_results]
    counts = [result[1] for result in satisfied_results]
    data = {'top_members': top_members, 'counts': counts}
    return json.dumps(data)
  
##Report## 


@app.route('/employee_report')
def employee_report():
    # Retrieve the required data
    employees = UserMembers.query.all()

    # Format the data into a report
    report_data = []
    for employee in employees:
        media = Media.query.filter_by(member_id=employee.id).first()
        if media:
            employee_data = {
                'Name': employee.name,
                'ID': employee.id,
                'Location': media.location_address,
                'Results': AnalysisResults.query.filter_by(media_id=media.id).first().results
            }
            report_data.append(employee_data)

    # Return the report data as JSON response
    return json.dumps(report_data)


####################End of Statistics####################



# Adding Media Analysis view 
@app.route('/pages/MediaAnalysis/')
@login_required
def pages_analysis():
  return render_template('pages/dashboard/mediaAnalysis.html', segment='media', parent='pages',user=current_user)

# Adding Media Analysis view 
@app.route('/pages/MediaAnalysisAudio/')
@login_required
def pages_analysis_audio():
  return render_template('pages/dashboard/mediaAnalysisAudio.html', segment='mediaAudio', parent='pages',user=current_user)

# Adding Media Analysis view 
@app.route('/pages/UploadAnalysis/')
@login_required
def pages_uploadMedia():
  return render_template('pages/dashboard/uploadMedia.html', segment='upload', parent='pages',user=current_user)

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