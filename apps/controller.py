from .models import *


class controller:
    def addUser(email, password):
        newUser = User(email=email, password=password)
        #newUser = User(email=email, password=password, name=name)
        db.session.add(newUser)
        db.session.commit()

    def editUser(id, email='', password='', name=''):
        user = User.query.filter_by(id=id).first()
        if email != '':
            user.email = email
        if password != '':
            user.password = password
        if name != '':
            user.name = name
        db.session.commit()

    def deleteUser(id):
        user = User.query.filter_by(id=id).first()
        db.session.delete(user)
        db.session.commit()

    def addUserLocation(name, companyName):
        newUserLocation = UserLocations(name=name, companyName=companyName)
        db.session.add(newUserLocation)
        db.session.commit()

    def editUserLocation(id, companyName = '', name=''):
        userLocation = UserLocations.query.filter_by(id=id).first()
        if companyName != '':
            userLocation.companyName = companyName
        if name != '':
            userLocation.name = name
        db.session.commit()

    def deleteUserLocation(id):
        userLocation = UserLocations.query.filter_by(id=id).first()
        db.session.delete(userLocation)
        db.session.commit()

    def addUserMember(name, companyName, member_id, member_gender, location_id=0):
        newUserMember = UserMembers(
            name=name, companyName = companyName, member_id = member_id, gender= member_gender, location_id=location_id)
        db.session.add(newUserMember)
        db.session.commit()

    def editUserMember(id, companyName = '' , name='', location_id=0):
        userMember = UserMembers.query.filter_by(id=id).first()
        if companyName != '':
            userMember.companyName = companyName
        if name != '':
            userMember.name = name
        if location_id != 0:
            userMember.location_id = location_id
        db.session.commit()

    def deleteUserMember(id):
        userMember = UserMembers.query.filter_by(id=id).first()
        db.session.delete(userMember)
        db.session.commit()

    def addMedia(media_name,url, type,companyName, location_address, member_id, results, detailed_results):
        newMedia = Media(media_name=media_name,url=url, type=type,companyName=companyName,
                         location_address=location_address, member_id=member_id, results =results, detailed_results=detailed_results) 
        db.session.add(newMedia)
        db.session.commit()

    def editMedia(id, url='', type='', companyName = '' , location_id=0, member_id=0):
        media = Media.query.filter_by(id=id).first()
        if companyName != '':
            media.companyName = companyName
        if url != '':
            media.url = url
        if location_id != 0:
            media.location_id = location_id
        if member_id != 0:
            media.member_id = member_id
        if type != '':
            media.type = type
        db.session.commit()

    def deleteMedia(id):
        media = Media.query.filter_by(id=id).first()
        db.session.delete(media)
        db.session.commit()

    def addAnalysisResult(media_id, result=''):
        newAnalysisResult = AnalysisResults(media_id=media_id, result=result)
        db.session.add(newAnalysisResult)
        db.session.commit()

    def editAnalysisResult(id, media_id=0, result=''):
        analysisResult = AnalysisResults.query.filter_by(id=id).first()
        if media_id != 0:
            analysisResult.media_id = media_id
        if result != '':
            analysisResult.result = result
        db.session.commit()

    def deleteAnalysisResult(id):
        analysisResult = AnalysisResults.query.filter_by(id=id).first()
        db.session.delete(analysisResult)
        db.session.commit()

        
# Add Feedback
    def AddFeedback(name, email, message):
        existing_feedback = Feedback.query.filter_by(message=message).first() #email=email
        if existing_feedback:
            # A feedback with the same email already exists, you can choose to update it or skip adding a new record
            # Update the existing record
            existing_feedback.name = name
            existing_feedback.email = email
            #existing_feedback.message = message
            db.session.commit()
        else:
            # No existing feedback with the same email, create a new record
            feedback = Feedback(name=name, email=email, message=message)
            db.session.add(feedback)
            db.session.commit()

        
        
    #Add Contact
    def AddContact(email, message):
        existing_contact = Contact.query.filter_by(message=message).first()  #email=email
        if existing_contact:
            # A contact with the same email already exists, you can choose to update it or skip adding a new record
            # Update the existing record
            #existing_contact.message = message
            existing_contact.email = email
            db.session.commit()
        else:
            # No existing contact with the same email, create a new record
            contact = Contact(email=email, message=message)
            db.session.add(contact)
            db.session.commit()
