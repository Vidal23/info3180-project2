"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""
import os, datetime, random, re
from app import app, db
from flask import render_template, request, redirect, url_for, flash,jsonify, make_response,session,abort
from forms import ProfileForm
from models import UserProfile
from werkzeug.utils import secure_filename


###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html')


@app.route("/profile", methods=["GET", "POST"])
def newProfile():
    
    form = ProfileForm()
    
    if request.method == 'GET':
        return render_template('newProfile.html', form=form)
    elif request.method == 'POST':
        if form.validate_on_submit():
            firstname = form.firstname.data
            lastname = form.lastname.data
            gender = form.gender.data
            email = form.email.data
            location = form.location.data
            bio = form.bio.data
            dateCreated = datetime.date.today()
            
            photo = form.photo.data
            filename = secure_filename(photo.filename)
            photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            userid = generateUserId(firstname, lastname)
            
            newUser = UserProfile(userid=userid, first_name=firstname, last_name=lastname, 
            gender=gender, email= email,location= location, biography=bio, pic=filename, created_on=dateCreated)
                
            db.session.add(newUser)
            db.session.commit()
            
            flash("Profile Successfully Created", "success")
            return redirect(url_for("profiles"))

"""@app.route('/profile/<userid>', methods=['GET', 'POST'])
def viewProfile(userid):
    user = UserProfile.query.filter_by(userid=userid).first()
    
    if request.method == 'GET':
        if user is not None:
            return render_template("profile.html", user=user)
        else:
            flash('User Not Found', 'danger')
            return redirect(url_for("home"))
            
    elif request.method == 'POST':
        if user is not None:
            response = make_response(jsonify(userid=user.userid, username=user.username, image=user.pic, gender=user.gender, age=user.age,
                    profile_created_on=user.created_on))
            response.headers['Content-Type'] = 'application/json'            
            return response
        else:
            flash('User Not Found', 'danger')
            return redirect(url_for("home"))"""

@app.route('/profile/<userid>')
def profile(userid):
    user = UserProfile.query.filter_by(userid=userid).first()
    return render_template('profile.html',user=user)
            
            
@app.route('/profiles', methods=['GET', 'POST'])
def profiles():
    user_list = UserProfile.query.all()
    users = [{"First Name": user.first_name, "Last Name": user.last_name, "userid": user.userid} for user in user_list]
    
    if request.method == 'GET':
        if user_list is not None:
            return render_template("profiles.html", users=user_list)
        else:
            flash('No Users Found', 'danger')
            return redirect(url_for("home"))
            
    elif request.method == 'POST':
        if user_list is not None:
            response = make_response(jsonify({"users": users}))                                           
            response.headers['Content-Type'] = 'application/json'            
            return response
        else:
            flash('No Users Found', 'danger')
            return redirect(url_for("home"))  
  
def generateUserId(firstname, lastname):
    temp = re.sub('[.: -]', '', str(datetime.datetime.now()))
    temp = list(temp)
    temp.extend(list(map(ord,firstname)))
    temp.extend(list(map(ord,lastname)))
    random.shuffle(temp)
    temp = list(map(str,temp))
    return int("".join(temp[:7]))%10000000 

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)

@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="8080")
