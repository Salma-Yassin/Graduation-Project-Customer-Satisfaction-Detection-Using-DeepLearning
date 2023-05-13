# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

# Flask modules
from flask   import render_template, request, flash, redirect, url_for, jsonify
import json
from jinja2  import TemplateNotFound
from .models import *
from flask_login import login_user, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import db 
from random import sample 
from .inferenceflask import query, query_face,query_body
import sys
from .controller import controller
from .helpers import unify_audio, unify_video, normalize_dict
from werkzeug.utils import secure_filename
import os
import imghdr
import magic
# App modules
from apps import app

@app.route('/data') # this is a dummy api that should be removed 
@login_required
def get_chart_data():
   # generating random data for testing 
   f = open("apps\Media_data.json")
   return json.load(f)


@app.route('/update_chart_raw', methods=['GET', 'POST'])
def update_chart_raw():

  if request.method == 'GET':
    with open("apps/updateChartRaw.json") as f:
       data = json.load(f)
    return data
  
  elif request.method == 'POST':
    data = request.get_json()
    with open("apps/updateChartRaw.json", "w") as f:
      json.dump(data, f)
    return jsonify({'status': 'success'})
   

@app.route('/location_data')
@login_required
def get_location_data():
   locations_table = UserLocations.query.filter_by(user_id= current_user.id).all()
   print(locations_table[0].name)
   return jsonify(locations_table)

@app.route('/empolyee_data')
@login_required
def get_empolyee_data():
   empolyee_table = UserMembers.query.filter_by(user_id= current_user.id).all()
   return jsonify(empolyee_table)

@app.route('/media_data')
@login_required
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
  media_name = request.form.get('media_name')
  url = request.form.get('url')
  url_check = Media.query.filter_by(url=url).first()

  media_type = request.form.get('media_type_form')
  media_name_check = Media.query.filter_by(media_name = media_name).first()
  emp_id = request.form.get('employee_id')
  location_add = request.form.get('location')

  if media_name_check:
     flash('Media Name used, enter another one', category='error')
  else: 
      if media_type == 'Audio':
          category = query(url)
          # Convert dictionary to string
          detailed_results = json.dumps(category)
          results = (category)[0]['label']
          results = unify_audio(results)


      elif media_type == 'video':
          category = query_face(url)
          # Convert dictionary to string
          detailed_results = json.dumps(normalize_dict(category))
          #results = list(category.keys())[0]
          results = next(iter(category))
          results = unify_video(results)
          #results = category[0]
      #category = query_face(url)
      #category = 'Unknown'
      # call body model ---> 

      elif media_type == 'Video':
         category = query_body(url)
         results = category
         detailed_results=results
      else:
        category = 'Unknown'

      user_id = current_user.id
      controller.addMedia(media_name = media_name, url = url , type = media_type, user_id = user_id, location_address = location_add, member_id = emp_id, results = results, detailed_results= detailed_results)
      flash('Media added successfuly!', category='success')
  

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
@app.route('/displayr/<filename>')
def display_videor(filename):
	#print('display_video filename: ' + filename)
	return redirect(url_for('debug_exp', filename='results/' + filename), code=301)
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

# Adding Media Analysis view 
@app.route('/pages/MediaAnalysis/')
@login_required
def pages_analysis():
  return render_template('pages/dashboard/mediaAnalysis.html', segment='media', parent='pages',user=current_user)

############################################################
@app.route('/pages/upload/')
def upload_form():
	return render_template('/pages/upload.html')

@app.route('/pages/upload/', methods=['POST'])
@login_required
def upload_video():
	if 'file' not in request.files:
		flash('No file part')
		return redirect(request.url)
	file = request.files['file']
	if file.filename == '':
		flash('No image selected for uploading')
		return redirect(request.url)
	else:
		filename = secure_filename(file.filename)
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		#print('upload_video filename: ' + filename)
		flash('Video successfully uploaded and displayed below')
		return render_template('/pages/dashboard/uploadMedia.html', filename=filename, segment='upload', parent='pages',user=current_user)

@app.route('/display/<filename>')
def display_video(filename):
	#print('display_video filename: ' + filename)
	return redirect(url_for('static', filename='uploads/' + filename), code=301)
#############################################################################
# Adding Media Analysis view 
@app.route('/pages/MediaAnalysisAudio/')
@login_required
def pages_analysis_audio():
  return render_template('pages/dashboard/mediaAnalysisAudio.html', segment='mediaAudio', parent='pages',user=current_user)

# Adding Media Analysis view 
@app.route('/pages/UploadAnalysis/', methods=['GET', 'POST'])
@login_required
def pages_uploadMedia():
    if request.method == 'POST':
        emp_id = request.form['employee_id']
        location_add = request.form['location']
        # Check which upload method was selected
        upload_method = request.form['upload-method']
        if upload_method == 'url':
            # Handle URL upload
            url = request.form['url']
            media_name = request.form['media_name']
            media_type = request.form['media_type']
            # employee_id = request.form['employee_id']
            # location = request.form['location']
            # Do something with the form data...
            category = query_face(url)
            detailed_results = json.dumps(category)
            results = (category)[0]['label']
            results = unify_audio(results)
            controller.addMedia(media_name = media_name, url =url , type = media_type, user_id = user_id, location_address = location_add, member_id = emp_id, results = results, detailed_results= detailed_results)
        elif upload_method == 'file':
            # Handle file upload
            file = request.files['file']
            mime_type = magic.from_buffer(file.read(1024), mime=True)
            file.seek(0)
            if mime_type.startswith('image'):
                # Handle image upload
                image_type = imghdr.what(file)
                if image_type:
                   
                    # The file is an image
                    # Do something with the image...
                   category = query_body(file)
                   results = category
                   detailed_results=results 
                   controller.addMedia(media_name = media_name, url ='' , type = media_type, user_id = user_id, location_address = location_add, member_id = emp_id, results = results, detailed_results= detailed_results)
                else:
                   raise TypeError
                    # The file is not a valid image
                    # Show an error message
            elif mime_type.startswith('video'):
               category = query_body(file)
               results = category
               detailed_results=results
               user_id = current_user.id
               controller.addMedia(media_name = media_name, url ='' , type = media_type, user_id = user_id, location_address = location_add, member_id = emp_id, results = results, detailed_results= detailed_results)
                # Handle video upload
                # Do something with the video...
            else:
               raise TypeError
                # The file is not an image or a video
                # Show an error message
        # Redirect to a success page or show an error message
    return render_template('pages/dashboard/uploadMedia.html', segment='upload', parent='pages', user=current_user)


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