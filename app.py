from crypt import methods
from flask import Flask, render_template, url_for, request, flash, session, redirect, g
from flask_sqlalchemy import SQLAlchemy
#user object inherithing from UxerMixin(helps users log in)
from flask_login import UserMixin
from sqlalchemy import null
from sqlalchemy.sql import func
#encrypts passwords 
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user, LoginManager

import urllib.request
from PIL import Image
import base64
import io
#using current_user object to access all of the info about the currently logged in user

#hashing function is a one way function that does not have an inverse(like math)
    #password -> hash password
    #but can't hash password -> password


app = Flask(__name__)


#storing databse in this folder
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

db = SQLAlchemy(app)


#
#db.Model is blueprint for an object thats going to stored in database(all notes need to look like this)
class Note(db.Model):
    #all users vitamins have unique ids
        #autimatically sets id
    id = db.Column(db.Integer, primary_key = True)
    vitamin = db.Column(db.String(10))
    data = db.Column(db.String(1000))
    description = db.Column(db.String(10000))
    #using func to set time of added vitamin
    date = db.Column(db.DateTime(timezone = True), default=func.now())
    #associating vitamins with user with foreign key(references a column of another database)
        #by storing id of user into this note
            #always references the user
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


#can create another thing to store like
#class Reminder(db.Model)
    #have to give it proper atributes(look at sqlalchemy.com) and foreignKey for one to many relationship

#how we're storing user input into database
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(150), unique = True)
    name = db.Column(db.String(150))
    password = db.Column(db.String(150))
    #tell every time we create vitamin add in that vitamin id into notes(storing all of users vitamins here)
        #using relationship to referance name of class
            #like a list
    notes = db.relationship('Note')

#setting up login manager
login_manager = LoginManager()
#Where do we need to go if not logged in(to login page)
login_manager.login_view = 'login' #or '/login
#which app we're using
login_manager.init_app(app)

#using this function to load user
    #telling flask how to load a user(telling flask what user we're looking)
@login_manager.user_loader
def load_user(id):
    #looking for primary key
    return User.query.get(int(id))




@app.route("/home", methods = ['GET', 'POST'])
def home():
    #current user is checking if there's currenlty a user logged in
    
    #to check if user has already been evaluated
    checked = 0
    ''' SESSION DOESNT TRACK SPECIFICALLY FOR USER SO MIGHT CHECK FOR SOMETHING IN THE DATABASE TO SEE IF THEY ALREADY TOOK THE TEST
    if "checked" in session:
        print("checcking for sessino checking")
        checked = session["checked"]
        print(checked)
        '''
    #maybe try QUERING vitamins from database to see if we queried anything
    new_vitamin = Note.query.filter_by(user_id = current_user.id).all()
    
    #IT WORKED!!! :))
    for i in new_vitamin:
        
        if i.vitamin == "heart" or "Immune-Rmor" or "Gastro-Digest II" or "Kalmz" or "ReGenerZyme Adrenal" or "ReGenerZyme Thyroid":
            checked = 1
        
    return render_template('home.html', user = current_user, checked = checked)

@app.route("/eval", methods = ['POST', 'GET'])
def eval():
    


    '''if evaluated == True:
        db.session.delete(new_vitamin)
        db.session.commit()
        evaluated = False


    #if its the first time running evaluation
    evaluated = True'''

    print("Im here")
    #the different types of vitamins
    heart = 0
    heart_description = "The heart is the hardest working muscle of the body. It continually contracts and relaxes (beating over 100,000 times every day), delivering life-giving blood to every organ, gland, cell, and structure of the body. ReGenerZyme Heart supports and restores the heart as well as other muscles of the body. It is excellent nutrition for athletes and others who want to optimize heart and muscle function."
    
    immune = 0
    immune_description = "Immune-Rmor (immune armor) is immune system support and restoration formula that nourishes the spleen, lymph, pituitary, and thymus glands. A healthy immune system is able to distinguish between a healthy cell and tissue and unwanted invaders. It is our body’s armor against unwanted bacteria, viruses, parasites, fungi, etc."

    gastro = 0
    gastro_description = "Gastro-Digest II is a two-stage formula designed to support digestion. The first stage assists the stomach where acid is used to break down proteins. The second stage of the formula is enteric coated, which protects the ingredients from the stomach acid. They remain intact to be utilized by the gallbladder, liver, pancreas and intestine where the major part of digestion and nutrient assimilation occurs."
    
    kalmz = 0
    kalmz_description = "Kalmz provides nutritional support for the body that needs to release physical pain and emotional stress. It also calms the toxic chaos that may overwhelm the body by denaturing (neutralizing) toxins from food, emotions, and/or the environment."
    
    adrenal = 0
    adrenal_description = "When stress is high and hormones are low the adrenals come to the rescue. ReGenerZyme Adrenal provides nutritional resources so the adrenals can rest, restore and function optimally. The 7-Keto DHEA in the formula supports both the thyroid and adrenals."
    
    thyroid = 0
    thyroid_description = "The thyroid is involved in producing hormones necessary for a stable emotional state, optimal metabolism, and normal body function. ReGenerZyme Thyroid was formulated to support the body with nutrients used to hydrate, balance, and restore the energy of the thyroid so it can function optimally."

    if request.method == 'POST':

        if request.form['submit_button'] == 'checked':
            flash('Evaluation complete!, click results to see results', category='success')

        for i in range(8):
            if request.form.get('heart' + str(i)):
                heart += 1
        #for checkboxes with same values
        #if request.form.get('inspira0'):
            #heart += 1

        for i in range(8):
            if request.form.get('immune' + str(i)):
                immune += 1

        for i in range(6):
            if request.form.get('gastro' + str(i)):
                gastro += 1

        for i in range(8):
            if request.form.get('kalmz' + str(i)):
                kalmz += 1

        for i in range(7):
            if request.form.get('adrenal' + str(i)):
                adrenal += 1

        for i in range(7):
            if request.form.get('thyroid' + str(i)):
                thyroid += 1

        #avoiding repeating questions
        #high cholesterol
        if request.form.get('adrenal1'):
            thyroid += 1

        #unhealthy food
        if request.form.get('immune2'):
            thyroid += 1

        #depression
        if request.form.get('kalmz1'):
            thyroid += 1
        
        #irregular or no mestrual cycles
        if request.form.get('adrenal6'):
            thyroid += 1

        if request.form.get('adrenal2'):
            immune += 1

        
            #vitamin = "heart",
            #the vitamin
            #how many to take
            #description
        #ITS RUNNING NOW!! no need to do sessions anymore, BUT THE BUTTON DOESN'T WORK!!!
        if heart >= 8:
            
            new_vitamin = Note(vitamin = "ReGenerZyme Heart", data = "you need 3 capsules before bed and 3 in the morning", description = heart_description, user_id = current_user.id)
            db.session.add(new_vitamin)
            db.session.commit()

        elif heart >= 5:
            
            new_vitamin = Note(vitamin = "ReGenerZyme Heart", data = "you need 2 capsules before bed and 2 in the morning", description = heart_description, user_id = current_user.id)
            db.session.add(new_vitamin)
            db.session.commit()

        elif heart >= 3:
            
            new_vitamin = Note(vitamin = "ReGenerZyme Heart", data = "you need 1 capsule before bed and 1 in the morning",description = heart_description, user_id = current_user.id)
            db.session.add(new_vitamin)
            db.session.commit()




        if immune == 8:
            new_vitamin = Note(vitamin = "Immune-Rmor", data = "you need 3 capsule before bed and 3 in the morning",description = immune_description, user_id = current_user.id)
            db.session.add(new_vitamin)
            db.session.commit()

        elif immune >= 5:
            new_vitamin = Note(vitamin = "Immune-Rmor", data = "you need 2 capsule before bed and 2 in the morning",description = immune_description, user_id = current_user.id)
            db.session.add(new_vitamin)
            db.session.commit()

        elif immune >= 2:
            new_vitamin = Note(vitamin = "Immune-Rmor", data = "you need 1 capsule before bed and 1 in the morning",description = immune_description, user_id = current_user.id)
            db.session.add(new_vitamin)
            db.session.commit()


        if gastro == 6:
            new_vitamin = Note(vitamin = "Gastro-Digest II", data = "you need 3 capsule before bed and 3 in the morning",description = gastro_description, user_id = current_user.id)
            db.session.add(new_vitamin)
            db.session.commit()

        elif gastro >=3:
            new_vitamin = Note(vitamin = "Gastro-Digest II", data = "you need 2 capsule before bed and 2 in the morning",description = gastro_description, user_id = current_user.id)
            db.session.add(new_vitamin)
            db.session.commit()

        elif gastro >= 1:
            new_vitamin = Note(vitamin = "Gastro-Digest II", data = "you need 1 capsule before bed and 1 in the morning",description = gastro_description, user_id = current_user.id)
            db.session.add(new_vitamin)
            db.session.commit()


        if kalmz == 8:#take more at night
            new_vitamin = Note(vitamin = "Kalmz", data = "you need 4 capsule before bed",description = kalmz_description, user_id = current_user.id)
            db.session.add(new_vitamin)
            db.session.commit()

        elif kalmz >=4:
            new_vitamin = Note(vitamin = "Kalmz", data = "you need 3 capsule before bed",description = kalmz_description, user_id = current_user.id)
            db.session.add(new_vitamin)
            db.session.commit()

        elif kalmz >= 1:
            new_vitamin = Note(vitamin = "Kalmz", data = "you need 2 capsule before bed",description = kalmz_description, user_id = current_user.id)
            db.session.add(new_vitamin)
            db.session.commit()


        if adrenal == 7:
            new_vitamin = Note(vitamin = "ReGenerZyme Adrenal", data = "you need 1 capsule before bed and 1 in the morning",description = adrenal_description, user_id = current_user.id)
            db.session.add(new_vitamin)
            db.session.commit()

        elif adrenal >=4:
            new_vitamin = Note(vitamin = "ReGenerZyme Adrenal", data = "you need 1 capsule before bed and 1 in the morning",description = adrenal_description, user_id = current_user.id)
            db.session.add(new_vitamin)
            db.session.commit()

        elif adrenal >= 1:
            new_vitamin = Note(vitamin = "ReGenerZyme Adrenal", data = "you need 1 capsule before bed and 1 in the morning",description = adrenal_description, user_id = current_user.id)
            db.session.add(new_vitamin)
            db.session.commit()


        if thyroid >= 8:
            new_vitamin = Note(vitamin = "ReGenerZyme Thyroid", data = "you need 3 capsule before bed",description = thyroid_description, user_id = current_user.id)
            db.session.add(new_vitamin)
            db.session.commit()

        elif thyroid >=4:
            new_vitamin = Note(vitamin = "ReGenerZyme Thyroid", data = "you need 2 capsule before bed",description = thyroid_description, user_id = current_user.id)
            db.session.add(new_vitamin)
            db.session.commit()

        elif thyroid >= 1:
            new_vitamin = Note(vitamin = "ReGenerZyme Thyroid", data = "you need 1 capsule before bed",description = thyroid_description, user_id = current_user.id)
            db.session.add(new_vitamin)
            db.session.commit()

        
    #session['heart'] = heart

    #maybe request.form(button here to take me to /results)
        
    return render_template("eval.html", user = current_user, heart = heart)

#to evaluate again HAVE TO DELETE PREVIOUS VITAMINS
@app.route("/eval_again", methods = ['POST', 'GET'])
def eval_again():
    

    #DELETING PREVIOUS VITAMIN IF TAKE EVALUATION AGAIN
    '''This issn't working 
        '''
    #THIS WORKS!!!! DELETING EVERY VITAMIN WHEN TAKING EVALUATION AGAIN
    #new_vitamin = Note.query.filter_by(user_id = current_user.id).all()

    #for i in new_vitamin:
       # db.session.delete(i)
       # db.session.commit()
        

    



    #notes.User.query().delete()

    #db.session.query(Note).filter(Note.id==current_user).delete()
    #db.session.commit()

    print("DELETED")

    #the different types of vitamins
    heart = 0
    heart_description = "The heart is the hardest working muscle of the body. It continually contracts and relaxes (beating over 100,000 times every day), delivering life-giving blood to every organ, gland, cell, and structure of the body. ReGenerZyme Heart supports and restores the heart as well as other muscles of the body. It is excellent nutrition for athletes and others who want to optimize heart and muscle function."
    
    immune = 0
    immune_description = "Immune-Rmor (immune armor) is immune system support and restoration formula that nourishes the spleen, lymph, pituitary, and thymus glands. A healthy immune system is able to distinguish between a healthy cell and tissue and unwanted invaders. It is our body’s armor against unwanted bacteria, viruses, parasites, fungi, etc."

    gastro = 0
    gastro_description = "Gastro-Digest II is a two-stage formula designed to support digestion. The first stage assists the stomach where acid is used to break down proteins. The second stage of the formula is enteric coated, which protects the ingredients from the stomach acid. They remain intact to be utilized by the gallbladder, liver, pancreas and intestine where the major part of digestion and nutrient assimilation occurs."
    
    kalmz = 0
    kalmz_description = "Kalmz provides nutritional support for the body that needs to release physical pain and emotional stress. It also calms the toxic chaos that may overwhelm the body by denaturing (neutralizing) toxins from food, emotions, and/or the environment."
    
    adrenal = 0
    adrenal_description = "When stress is high and hormones are low the adrenals come to the rescue. ReGenerZyme Adrenal provides nutritional resources so the adrenals can rest, restore and function optimally. The 7-Keto DHEA in the formula supports both the thyroid and adrenals."
    
    thyroid = 0
    thyroid_description = "The thyroid is involved in producing hormones necessary for a stable emotional state, optimal metabolism, and normal body function. ReGenerZyme Thyroid was formulated to support the body with nutrients used to hydrate, balance, and restore the energy of the thyroid so it can function optimally."

    if request.method == 'POST':

        #THIS WORKS BUT DOESN SPECIFICALLY TRACK if SPECIFIC USERS HAVE TAKEN THE TEST
        
        if request.form['submit_button'] == 'checked':
            #flashing message when user submits their evalutation
            flash('Evaluation complete!, click results to see results', category='success')

            #deleting their previous vitamins when they press the submit button again
            #THIS WORKS!!!! DELETING EVERY VITAMIN WHEN TAKING EVALUATION AGAIN
            new_vitamin = Note.query.filter_by(user_id = current_user.id).all()

            for i in new_vitamin:
                db.session.delete(i)
                db.session.commit()
        

        for i in range(8):
            if request.form.get('heart' + str(i)):
                heart += 1
        #for checkboxes with same values
        #if request.form.get('inspira0'):
            #heart += 1

        for i in range(8):
            if request.form.get('immune' + str(i)):
                immune += 1

        for i in range(6):
            if request.form.get('gastro' + str(i)):
                gastro += 1

        for i in range(8):
            if request.form.get('kalmz' + str(i)):
                kalmz += 1

        for i in range(7):
            if request.form.get('adrenal' + str(i)):
                adrenal += 1

        for i in range(7):
            if request.form.get('thyroid' + str(i)):
                thyroid += 1

        #avoiding repeating questions
        #high cholesterol
        if request.form.get('adrenal1'):
            thyroid += 1

        #unhealthy food
        if request.form.get('immune2'):
            thyroid += 1

        #depression
        if request.form.get('kalmz1'):
            thyroid += 1
        
        #irregular or no mestrual cycles
        if request.form.get('adrenal6'):
            thyroid += 1

        if request.form.get('adrenal2'):
            immune += 1

        
            #vitamin = "heart",
            #the vitamin
            #how many to take
            #description
        #ITS RUNNING NOW!! no need to do sessions anymore, BUT THE BUTTON DOESN'T WORK!!!
        if heart >= 8:
            
            new_vitamin = Note(vitamin = "ReGenerZyme Heart", data = "You need 3 capsules before bed and 3 in the morning", description = heart_description, user_id = current_user.id)
            db.session.add(new_vitamin)
            db.session.commit()

            #flash('Evaluation complete!, click results to see results', category='success')
        elif heart >= 5:
            
            new_vitamin = Note(vitamin = "ReGenerZyme Heart", data = "You need 2 capsules before bed and 2 in the morning", description = heart_description, user_id = current_user.id)
            db.session.add(new_vitamin)
            db.session.commit()

            #flash('Evaluation complete!, click results to see results', category='success')
        elif heart >= 3:
            
            new_vitamin = Note(vitamin = "ReGenerZyme Heart", data = "You need 1 capsule before bed and 1 in the morning",description = heart_description, user_id = current_user.id)
            db.session.add(new_vitamin)
            db.session.commit()

            #flash('Evaluation complete!, click results to see results', category='success')



        if immune == 8:
            new_vitamin = Note(vitamin = "Immune-Rmor", data = "You need 3 capsule before bed and 3 in the morning",description = immune_description, user_id = current_user.id)
            db.session.add(new_vitamin)
            db.session.commit()

            #flash('Evaluation complete!, click results to see results', category='success')
        elif immune >= 5:
            new_vitamin = Note(vitamin = "Immune-Rmor", data = "You need 2 capsule before bed and 2 in the morning",description = immune_description, user_id = current_user.id)
            db.session.add(new_vitamin)
            db.session.commit()

            #flash('Evaluation complete!, click results to see results', category='success')
        elif immune >= 2:
            new_vitamin = Note(vitamin = "Immune-Rmor", data = "You need 1 capsule before bed and 1 in the morning",description = immune_description, user_id = current_user.id)
            db.session.add(new_vitamin)
            db.session.commit()

            #flash('Evaluation complete!, click results to see results', category='success')

        if gastro == 6:
            new_vitamin = Note(vitamin = "Gastro-Digest II", data = "You need 3 capsule before bed and 3 in the morning",description = gastro_description, user_id = current_user.id)
            db.session.add(new_vitamin)
            db.session.commit()

            #flash('Evaluation complete!, click results to see results', category='success')
        elif gastro >=3:
            new_vitamin = Note(vitamin = "Gastro-Digest II", data = "You need 2 capsule before bed and 2 in the morning",description = gastro_description, user_id = current_user.id)
            db.session.add(new_vitamin)
            db.session.commit()

            #flash('Evaluation complete!, click results to see results', category='success')
        elif gastro >= 1:
            new_vitamin = Note(vitamin = "Gastro-Digest II", data = "You need 1 capsule before bed and 1 in the morning",description = gastro_description, user_id = current_user.id)
            db.session.add(new_vitamin)
            db.session.commit()

            #flash('Evaluation complete!, click results to see results', category='success')

        if kalmz == 8:#take more at night
            new_vitamin = Note(vitamin = "Kalmz", data = "You need 4 capsule before bed",description = kalmz_description, user_id = current_user.id)
            db.session.add(new_vitamin)
            db.session.commit()

            #flash('Evaluation complete!, click results to see results', category='success') 
        elif kalmz >=4:
            new_vitamin = Note(vitamin = "Kalmz", data = "You need 3 capsule before bed",description = kalmz_description, user_id = current_user.id)
            db.session.add(new_vitamin)
            db.session.commit()

            #flash('Evaluation complete!, click results to see results', category='success')
        elif kalmz >= 1:
            new_vitamin = Note(vitamin = "Kalmz", data = "You need 2 capsule before bed",description = kalmz_description, user_id = current_user.id)
            db.session.add(new_vitamin)
            db.session.commit()

            #flash('Evaluation complete!, click results to see results', category='success')

        if adrenal == 7:
            new_vitamin = Note(vitamin = "ReGenerZyme Adrenal", data = "You need 1 capsule before bed and 1 in the morning",description = adrenal_description, user_id = current_user.id)
            db.session.add(new_vitamin)
            db.session.commit()

            #flash('Evaluation complete!, click results to see results', category='success')
        elif adrenal >=4:
            new_vitamin = Note(vitamin = "ReGenerZyme Adrenal", data = "You need 1 capsule before bed and 1 in the morning",description = adrenal_description, user_id = current_user.id)
            db.session.add(new_vitamin)
            db.session.commit()

            #flash('Evaluation complete!, click results to see results', category='success')
        elif adrenal >= 1:
            new_vitamin = Note(vitamin = "ReGenerZyme Adrenal", data = "You need 1 capsule before bed and 1 in the morning",description = adrenal_description, user_id = current_user.id)
            db.session.add(new_vitamin)
            db.session.commit()

            #flash('Evaluation complete!, click results to see results', category='success')

        if thyroid >= 8:
            new_vitamin = Note(vitamin = "ReGenerZyme Thyroid", data = "You need 3 capsule in the morning",description = thyroid_description, user_id = current_user.id)
            db.session.add(new_vitamin)
            db.session.commit()

            #flash('Evaluation complete!, click results to see results', category='success')
        elif thyroid >=4:
            new_vitamin = Note(vitamin = "ReGenerZyme Thyroid", data = "You need 2 capsule in the morning",description = thyroid_description, user_id = current_user.id)
            db.session.add(new_vitamin)
            db.session.commit()

            #flash('Evaluation complete!, click results to see results', category='success')
        elif thyroid >= 1:
            new_vitamin = Note(vitamin = "ReGenerZyme Thyroid", data = "You need 1 capsule in the morning",description = thyroid_description, user_id = current_user.id)
            db.session.add(new_vitamin)
            db.session.commit()

            #flash('Evaluation complete!, click results to see results', category='success')
        
    #session['heart'] = heart

    #maybe request.form(button here to take me to /results)
        
    return render_template("eval.html", user = current_user, heart = heart)

@app.route("/results")
def results():

    #MAYBE PUT ALL OF IMAGES IN LIST AND RUN FOR LOOP IN HTML SO IMAGES COULD GO TO THE VERY TOP
    images = []

    #displaying pictures
    heart_im = None
    immune_im = None
    gastro_im = None
    kalmz_im = None
    

    #maybe have to query from database
    #vitamin = Note.query.get_or_404(id)
    #vitamin_list = Note.query.all()
    new_vitamin = Note.query.filter_by(user_id = current_user.id).all()

    heart_image = null
    immune_image = null
    gastro_image = null
    kalmz_image = null

    #for what images to pass
    for i in new_vitamin:
        
        if i.vitamin == "ReGenerZyme Heart":
            
            heart_im = Image.open("Heart.jpg")

        #using BytesIO we get the in-memory info to save the image we just read
            data_image = io.BytesIO()

        #saving it as JPEG
            heart_im.save(data_image, "JPEG")

        #Then encode saved image file.
            encoded_img_data = base64.b64encode(data_image.getvalue())
            heart_image = encoded_img_data.decode('utf-8')

            images.append(heart_image)

        if i.vitamin == "Immune-Rmor":
        
            
            immune_im = Image.open("Immune.jpg")

            #using BytesIO we get the in-memory info to save the image we just read
            data_image_immune = io.BytesIO()

            #saving it as JPEG
            immune_im.save(data_image_immune, "JPEG")

            #Then encode saved image file.
            encoded_img_data_immune = base64.b64encode(data_image_immune.getvalue())

            immune_image = encoded_img_data_immune.decode('utf-8')

            images.append(immune_image)

        if i.vitamin == "Gastro-Digest II":
        
            
            gastro_im = Image.open("gastro.jpg")

            #using BytesIO we get the in-memory info to save the image we just read
            data_image_gastro = io.BytesIO()

            #saving it as JPEG
            gastro_im.save(data_image_gastro, "JPEG")

            #Then encode saved image file.
            encoded_img_data_gastro = base64.b64encode(data_image_gastro.getvalue())

            gastro_image = encoded_img_data_gastro.decode('utf-8')

            images.append(gastro_image)

        if i.vitamin == "Kalmz":
        
            
            kalmz_im = Image.open("Kalmz.jpg")

            #using BytesIO we get the in-memory info to save the image we just read
            data_image_kalmz = io.BytesIO()

            #saving it as JPEG
            kalmz_im.save(data_image_kalmz, "JPEG")

            #Then encode saved image file.
            encoded_img_data_kalmz = base64.b64encode(data_image_kalmz.getvalue())

            kalmz_image = encoded_img_data_kalmz.decode('utf-8')

            images.append(kalmz_image)
        if i.vitamin == "ReGenerZyme Adrenal":
        
            
            adrenal_im = Image.open("adrenal.jpg")

            #using BytesIO we get the in-memory info to save the image we just read
            data_image_adrenal = io.BytesIO()

            #saving it as JPEG
            adrenal_im.save(data_image_adrenal, "JPEG")

            #Then encode saved image file.
            encoded_img_data_adrenal = base64.b64encode(data_image_adrenal.getvalue())

            adrenal_image = encoded_img_data_adrenal.decode('utf-8')

            images.append(adrenal_image)
        if i.vitamin == "ReGenerZyme Thyroid":
        
            
            thyroid_im = Image.open("Thyroid.jpg")

            #using BytesIO we get the in-memory info to save the image we just read
            data_image_thyroid = io.BytesIO()

            #saving it as JPEG
            thyroid_im.save(data_image_thyroid, "JPEG")

            #Then encode saved image file.
            encoded_img_data_thyroid = base64.b64encode(data_image_thyroid.getvalue())

            thyroid_image = encoded_img_data_thyroid.decode('utf-8')

            images.append(thyroid_image)
        
    
#heart_image = heart_image, immune_image = immune_image, gastro_image = gastro_image, kalmz_image = kalmz_image
    return render_template("results.html", user = current_user, images = images)


#home page
@app.route("/")
def index():
    return render_template("index.html")

#creating our login page
@app.route("/login", methods = ['GET', 'POST'])
def login():
    #getting user input
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        #getting emails from database by query to see if any match users input
            #if any do match store in user object
        user = User.query.filter_by(email=email).first() #gets the first email it matches

        #if did find user
        if user:
            #hashing both passwords and see if they match
            if check_password_hash(user.password, password):
                flash('Logged in succesfully', category = 'success')
                
                #logging in user and remembering that the user is logged in until clear website
                login_user(user, remember = True)
                #if logged in go to home page(somewhere else)
                return redirect("/home")

            #if hashed passwords don't match then
            else:
                flash('Incorrect password', category = 'error')
        #if there is no email to the one the user inputted then
        else: 
            flash('Email does not exist', category='error')

    return render_template("login.html", user = current_user)
    #dont really need current_user because we aren't using nav bar here




#creating register page
@app.route("/register", methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        #getting the forms
        email = request.form.get('email')
        name = request.form.get('name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        #checking to see if email already exist by comparing it to all emails in database
        user = User.query.filter_by(email=email).first()

        #if inputted an already exisisting email in database
        if user:
            flash('Email already exists', category = 'error')

        #too short of email
        if len(email) < 4:
            #flashing messages
            flash("Email must be greater than 4 charaters", category= "error")
        #too short of a name
        elif len(name) < 2:
            flash("name must be greater than 1 charater", category= "error")
        #password doesnt confirm
        elif password1 != password2:
            flash("passwords must be the same", category= "error")
        #password too short
        elif len(password1) < 7:
            flash("Password must be greater than 7 charaters", category= "error")
        #if input is adequate pass to database
        else:
            #creating new user object by using User class
                #hashing password 'sha256' hashing algorith
            #if user definately not exist then put them in database
                #if an account email doesn't have the same email then make database
            if db.session.query(User).filter_by(email=email).count() < 1:
                new_user = User(email = email, name = name, password = generate_password_hash(password1, method = 'sha256'))
                
                #adding user to database
                db.session.add(new_user)
                db.session.commit()
                #logging in user when they sign up
                login_user(new_user, remember = True)
                flash("Account created", category= "success")

                #going back to home page
                return redirect("/home")
    return render_template("register.html", user = current_user)
    #don't really need current_user here because we're not showing navbar

@app.route("/logout")
#can only access logout if logged in
@login_required
def logout():
    #function automatically logs out current user
    logout_user()
    #when user logs out redirecting back to sign in page
    return redirect("/login")


if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'

    app.run(debug=True, port = 9000)