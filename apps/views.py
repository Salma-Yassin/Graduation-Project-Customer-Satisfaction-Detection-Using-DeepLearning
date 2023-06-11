# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

# Flask modules
from flask import Flask, render_template, request, flash, redirect, url_for, jsonify
import json
from jinja2 import TemplateNotFound
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
from .inference_flask import query, query_face, queryLocal, query_body_video, query_body_image
import sys
from .controller import controller
from moviepy.editor import *
from .helpers import unify_audio, unify_video, normalize_dict, sorting_audio, sorting_video_face
from functools import wraps
from .TestEmotionDetector import extractIDfromURL
# App modules
from apps import app
import random
from datetime import datetime, timedelta
from sqlalchemy import case, Float

# Implement role-based access control
class Role:
    ADMIN = 'admin'
    REGULAR = 'regular'


# Define custom decorators for restricting access based on role
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        print("")
        if not current_user.is_authenticated or current_user.role != Role.ADMIN:
            return render_template('pages/examples/404.html'), 403
        return f(*args, **kwargs)
    return decorated_function

def createAdmins():
  new_user = AdminUser(email="Admin@gmail.com", companyName = 'blue', password= generate_password_hash("123456789", method='sha256')) 
  db.session.add(new_user)
  db.session.commit()
  return new_user
   
def create_user():
     new_user = RegularUser(email="help@gg", companyName = 'blue', password= generate_password_hash("123456789", method='sha256')) 
     db.session.add(new_user)
     db.session.commit()
     #login_user(new_user, remember=True)
     return new_user

def create_locations(user):
    locations = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Miami']
    user_locations = []
    for location in locations:
        user_location = UserLocations(name=location, companyName = user.companyName)
        db.session.add(user_location)
        db.session.commit()
        user_locations.append(user_location)
    return user_locations


def create_members(user, user_locations):
    members = []
    for i in range(10):
        member_id = random.randint(100000, 999999)
        gender = random.choice(['male', 'female'])
        location = random.choice(user_locations)
        member = UserMembers(name=f'Member{i}', companyName = user.companyName , member_id=member_id,
                             gender=gender, location_id=location.id)
        db.session.add(member)
        db.session.commit()
        members.append(member)
    return members


def create_media(user, user_locations, members):
    media_types = ['Audio', 'Video']
    results = ['Satisfied', 'Unsatisfied', 'Neutral']
    medias = []
    for i in range(100):
        member = random.choice(members)
        location = random.choice(user_locations)
        media_type = random.choice(media_types)
        result = random.choice(results)
        audio_results = "[{\"score\": 0.7873730659484863, \"label\": \"hap\"}, {\"score\": 0.20546337962150574, \"label\": \"ang\"}, {\"score\": 0.0037874202243983746, \"label\": \"sad\"}, {\"score\": 0.0033761027734726667, \"label\": \"neu\"}]"
        start_date = datetime(2023, 1, 1)
        end_date = datetime(2023, 12, 31)
        created_at = start_date + \
            timedelta(seconds=random.randint(
                0, int((end_date - start_date).total_seconds())))
        media = Media(media_name=f'Media {i}', url=f'https://media{i}.com',
                      location_address=location.name, member_id=member.member_id,
                      type=media_type, companyName = user.companyName ,created_at = created_at, results=result,
                      audio_results = audio_results)
        db.session.add(media)
        db.session.commit()
        medias.append(media)
        # Create analysis results for the media
        # analysis_results = AnalysisResults(media_id=media.id, results='Analysis Results')
        # db.session.add(analysis_results)
        # db.session.commit()
    return medias


@app.route('/data')  # this is a dummy api that should be removed
def get_chart_data():
    # generating random data for testing
    f = open("apps\Media_data.json")
    return json.load(f)


@app.route('/play_media', methods=['GET', 'POST'])
def play_media():

    if request.method == 'GET':
        with open("apps/updatePlayMedia.json") as f:
            data = json.load(f)
        return data

    elif request.method == 'POST':
        data = request.get_json()
        with open("apps/updatePlayMedia.json", "w") as f:
            json.dump(data, f)
        return jsonify({'status': 'success'})


@app.route('/update_chart_audio', methods=['GET', 'POST'])
def update_chart_audio():
    if request.method == 'GET':
        with open("apps/updateChartAudio.json") as f:
            data = json.load(f)
        return data

    elif request.method == 'POST':
        data = request.get_json()
        with open("apps/updateChartAudio.json", "w") as f:
            json.dump(data, f)
        return jsonify({'status': 'success'})

@app.route('/update_chart_face', methods=['GET', 'POST'])
def update_chart_face():
    if request.method == 'GET':
        with open("apps/updateChartFace.json") as f:
            data = json.load(f)
        return data

    elif request.method == 'POST':
        data = request.get_json()
        with open("apps/updateChartFace.json", "w") as f:
            json.dump(data, f)
        return jsonify({'status': 'success'})


@app.route('/update_chart_body', methods=['GET', 'POST'])
def update_chart_body():
    if request.method == 'GET':
        with open("apps/updateChartBody.json") as f:
            data = json.load(f)
        return data

    elif request.method == 'POST':
        data = request.get_json()
        with open("apps/updateChartBody.json", "w") as f:
            json.dump(data, f)
        return jsonify({'status': 'success'})

@app.route('/location_data')
@login_required
def get_location_data():
   locations_table = UserLocations.query.filter_by(companyName = current_user.companyName).all()
   return jsonify(locations_table)

@app.route('/empolyee_data')
@login_required
def get_empolyee_data():
   empolyee_table = UserMembers.query.filter_by(companyName = current_user.companyName).all()
   return jsonify(empolyee_table)

@app.route('/media_data')
@login_required
def get_media_data():
   # generating random data for testing 
   #cursor= db.cursor()
   #history_table = cursor.execute("SELECT * FROM Media WHERE user_id=?;", [current_user.id])
   history_table = Media.query.filter_by(companyName = current_user.companyName).all()
   return jsonify(history_table)
   #return jsonify({'data':[{'URL':'https://www.youtube.com/watch?v=poZt1f43gBc','Type':'vedio','Location':'Maady','EmployeeID' : '20147501'},{'URL':'https://www.youtube.com/watch?v=qDc484XBFjI','Type':'vedio','Location':'October','EmployeeID' : '201871501'},{'URL':'https://www.youtube.com/watch?v=qDc484XBFjI','Type':'vedio','Location':'October','EmployeeID' : '201871501'},{'URL':'https://www.youtube.com/watch?v=qDc484XBFjI','Type':'vedio','Location':'October','EmployeeID' : '201871501'},{'URL':'https://www.youtube.com/watch?v=qDc484XBFjI','Type':'vedio','Location':'October','EmployeeID' : '201871501'}]})


# Pages -- Dashboard
# @app.route('/', defaults={'path': 'dashboard.html'})
def add_media_function(request):
    # retrive fields from data base
    media_name = request.form.get('media_name')
    urlink = request.form.get('url')
    # url_check = Media.query.filter_by(url=url).first()
    # url = ""
    media_type = request.form.get('media_type_form')
    media_name_check = Media.query.filter_by(media_name=media_name).first()
    emp_id = request.form.get('employee_id')
    location_add = request.form.get('location')

    file=request.files.get('file')
    face_results=''
    body_results='' 
    audio_results=''
    redirect(url_for('loading_page'))
    if media_name_check:
        flash('Media Name used, enter another one', category='error')
    else: 
        if media_type == 'Audio':
            if file: 
                filename = secure_filename(file.filename)
                file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                print(file_path)
                url=file_path
                category=queryLocal(url)
                flash('File has been uploaded.')
                audio_results = json.dumps(sorting_audio(category))
                results = (category)[0]['label']
                results = unify_audio(results)

            elif urlink: 
                url=urlink
                category = query(url)
                # Convert dictionary to string
                audio_results = json.dumps(sorting_audio(category))
                results = (category)[0]['label']
                results = unify_audio(results)
        
        elif media_type == 'Video':
            if file: 
                filename = secure_filename(file.filename)
                file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                print(file_path)
                flag = 'local'
                url=file_path
                ## Bodyyyyyy
                category = query_body_video(url,media_name)
                body_results = category
                print('Body Model Results:', body_results)
                ###face
                category = query_face(url,flag,media_name)
                face_results = json.dumps(normalize_dict(sorting_video_face((category))))
                results = next(iter(category))
                results = unify_video(results)
                print('Face Model Results:',face_results)

                

                ## AUDIO
                video = VideoFileClip(url)
                audio = video.audio
                if (audio):
                    print("Audio Analysis Started")
                    output_audio = os.path.join(os.path.abspath(os.path.dirname(
                    __file__)), app.config['UPLOAD_FOLDER'],media_name,'.wav')
                    audio.write_audiofile(output_audio, codec='pcm_s16le')
                    category = queryLocal(output_audio)
                    print(category)
                    audio_results = json.dumps(category)
                    results = (category)[0]['label']
                    results = unify_audio(results)
                    print('Audio Model Results:', audio_results)
                else:
                    print('No audio exists!')
                video.close()

            elif urlink:
                url=urlink
                flag = 'url'
                category = query_face(url,flag,media_name)
                face_results = json.dumps(normalize_dict(sorting_video_face((category))))
                results = next(iter(category))
                results = unify_video(results)

                id = extractIDfromURL(url)
                url = "https://drive.google.com/uc?id=" + id
                video = VideoFileClip(url)
                audio = video.audio
                if (audio):
                    output_audio = os.path.join(os.path.abspath(os.path.dirname(
                    __file__)), app.config['UPLOAD_FOLDER'],media_name,'.wav')
                    audio.write_audiofile(output_audio, codec='pcm_s16le')
                    category = queryLocal(output_audio)
                    print(category)
                    audio_results = json.dumps(category)
                    # results = (category)[0]['label']
                    audio_results = unify_audio(results)
                    print('Audio Model Results:',audio_results)
                else:
                    print('No audio exists!')
                video.close()

            # Merge Function


        else:
            category = 'Unknown'
        

  
    companyName = current_user.companyName
    controller.addMedia(media_name = media_name, url = url , type = media_type, companyName = companyName, location_address = location_add, member_id = emp_id, 
                        results = results, face_results=face_results, body_results=body_results, audio_results=audio_results)
    flash('Media added successfuly!', category='success')
    
    #created_media = Media.query.filter_by(url=url).first()
     #controller.addAnalysisResult(media_id= created_media.id, result=category[0]['label'])    
     #show data 
     #return redirect(url_for('pages_history'))


@app.route('/employees', methods=['GET','POST'])
@login_required
def user_employees():
    # user=User.query.filter_by(id=current_user.id)
    # print(user)
    user=current_user
    companyName=current_user.companyName
    employees=UserMembers.query.filter_by(companyName=companyName).all()
    return render_template('pages/dashboard/useremployees.html',segment='useremployees', employees=employees,user=user)  

@app.route('/edit_user_employees/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_user_employees(id):
    user_member = UserMembers.query.filter_by(id=id).first()
    user_id = current_user.id
    print(user_id)
    locations = UserLocations.query.filter_by(companyName=current_user.companyName).all()
    
    if request.method == 'POST':
        name = request.form.get('name')
        location_id = request.form.get('location_id')
        controller.editUserMember(user_member.id, companyName=current_user.companyName, name=name, location_id=location_id)
        flash('Employee updated successfully', 'success')
        return redirect(url_for('user_employees'))

    return render_template('pages/dashboard/edit_useremployees.html', parent='pages', locations=locations, id=id, user_member=user_member, user=current_user)




@app.route('/delete_user_employees', methods=['POST'])
@login_required
def delete_user_employees():
    employee_id = request.form.get('employee_id')
    controller.deleteUserMember(employee_id)
    return redirect(url_for('user_employees'))

@app.route('/user_locations', methods=['GET','POST'])
@login_required
def user_Locations():
    # user=User.query.filter_by(id=current_user.id)
    # print(user)
    user=current_user
    companyName=current_user.companyName
    Locations=UserLocations.query.filter_by(companyName=companyName).all()
    return render_template('pages/dashboard/userlocations.html',segment='userlocations', Locations=Locations,user=user) 

@app.route('/edit_user_locations/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_user_locations(id):
    user_location = UserLocations.query.filter_by(id=id).first()
    user_id = current_user.id
    print(user_id)
    locations = UserLocations.query.filter_by(companyName=current_user.companyName).all()

    if request.method == 'POST':
        name = request.form.get('name')
        if name:
            controller.editUserLocation(id=id, companyName=current_user.companyName, name=name)
            flash('Location updated successfully', 'success')
            return redirect(url_for('user_Locations'))
    

    return render_template('pages/dashboard/edit_userlocationshtml', parent='pages', locations=locations, id=id, user_location=user_location, user=current_user)




@app.route('/delete_user_locations/<int:id>', methods=['POST'])
@login_required
def delete_user_locations(id):
    location_id = id
    controller.deleteUserLocation(location_id)
    flash('Location deleted successfully', 'success')
    return redirect(url_for('user_Locations'))



@app.route('/loading')
def loading_page():
    return render_template('pages/dashboard/loading.html')

@app.route('/', methods=['GET', 'POST'])
@login_required
def pages_dashboard():
  emp=UserMembers.query.filter_by(companyName=current_user.companyName).all()
  emp_loc=UserLocations.query.filter_by(companyName=current_user.companyName).all()
  user = AdminUser.query.filter_by(email="Admin@gmail.com").first()
  if user:
      print(f"User with email '{user.email}' already exists")
  else:
      # Create a new user object and add it to the database session
      user = createAdmins()
      user_locations = create_locations(user)
      members = create_members(user, user_locations)
      create_media(user, user_locations, members)

  if request.method == 'POST':
     add_media_function(request)
     return redirect(url_for('pages_history'))
  return render_template('pages/dashboard/dashboard.html', emp=emp,emp_loc=emp_loc,segment='dashboard', parent='pages', user=current_user)


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
@admin_required
def pages_manage():
  if request.method == 'POST':
     companyName = current_user.companyName
     if request.form.get('Location_form'):       
        location = request.form.get('location')
        controller.addUserLocation(name=location, companyName = companyName)

     elif request.form.get('Employee_form'):
        empo_name = request.form.get('name')
        empo_gender = request.form.get('gender')
        empo_id = request.form.get('id')
        empo_location = request.form.get('location')
        controller.addUserMember(name=empo_name, companyName = companyName , member_id=empo_id, member_gender=empo_gender, location_id=empo_location)
        
  return render_template('pages/dashboard/manage.html', segment='manage', parent='pages',user=current_user)

@app.route('/pages/support')
@login_required
def support_page():
  return render_template('pages/dashboard/support.html', segment='support', parent='pages',user=current_user)

##ِAdding About Us Page###
@app.route('/about')
def about():
    return render_template('pages/dashboard/about.html')

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
        .with_entities(
            Media.location_address,
            func.count(case((Media.results == 'Satisfied', 1))).label('count')
        )
        .group_by(Media.location_address)
        .order_by(func.count().desc())
        # .limit(5)  # to get top 5 locations
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
        .filter(Media.results == 'Satisfied')
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
    # # Retrieve the required data
    # employees = UserMembers.query.all()

    # # Format the data into a report
    # report_data = []
    # for employee in employees:
    #     media = Media.query.filter_by(member_id=employee.id).first()
    #     if media:
    #         employee_data = {
    #             'Name': employee.name,
    #             'ID': employee.id,
    #             'Location': media.location_address,
    #             # 'Results': AnalysisResults.query.filter_by(media_id=media.id).first().results
    #         }
    #         report_data.append(employee_data)

    # # Return the report data as JSON response
    # return json.dumps(report_data)
    return {}

####################End of Statistics####################



# Adding Media Analysis view 
@app.route('/pages/MediaAnalysis/<video>')
@login_required
def pages_analysis(video):
    filename = secure_filename(video)
    print(filename)
    return render_template('pages/dashboard/mediaAnalysis.html', face=filename+'_face.mp4',body=filename+'_body.mp4', segment='media', parent='pages', user=current_user)

# Adding Media Analysis view
@app.route('/display/<filename>')
def display_video(filename):
	#print('display_video filename: ' + filename)
	return redirect(url_for('static', filename='filat/' + filename), code=301)

@app.route('/pages/MediaAnalysisAudio/')
@login_required
def pages_analysis_audio():
    return render_template('pages/dashboard/mediaAnalysisAudio.html', segment='mediaAudio', parent='pages', user=current_user)

# Adding Media Analysis view


@app.route('/pages/UploadAnalysis/', methods=['GET', 'POST'])
@login_required
def pages_uploadMedia():
    return render_template('pages/dashboard/uploadMedia.html', segment='upload', parent='pages', user=current_user)


@app.route('/pages/settings/')
@login_required
def pages_settings():
    return render_template('pages/settings.html', segment='settings', parent='pages', user=current_user)
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
    # return render_template("sign-in.html", user=current_user)
    return render_template('accounts/sign-in.html', segment='sign_in', parent='accounts')


@app.route('/accounts/sign-up/', methods=['GET', 'POST'])
def accounts_sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        companyName = request.form.get('companyName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        # return render_template('pages/dashboard/dashboard.html', segment='dashboard', parent='pages')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
            # return render_template('pages/dashboard/dashboard.html', segment='dashboard', parent='pages')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
            # return render_template('pages/dashboard/dashboard.html', segment='dashboard', parent='pages')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
            # return render_template('pages/dashboard/dashboard.html', segment='dashboard', parent='pages')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
            # return render_template('pages/dashboard/dashboard.html', segment='dashboard', parent='pages')
        else:
            new_user = RegularUser(email = email, companyName = companyName , password = generate_password_hash(password1, method='sha256')) 
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


@app.route('/accounts/password-change/')
def accounts_password_change():
    return render_template('accounts/password-change.html', segment='password-change', parent='accounts')


@app.route('/accounts/logout/')
@login_required  # makes sure that the user is logged out only if they are logged in
def logout():
    logout_user()
    return redirect(url_for('accounts_sign_in'))
