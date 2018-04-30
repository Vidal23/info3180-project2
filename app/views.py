"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""
import os, datetime, random, re, jwt
from functools import wraps
from app import app, db, login_manager, token_key
from flask import render_template, request, redirect, url_for, flash,jsonify, g, make_response,session,abort
from forms import ProfileForm, LoginForm, PostForm
from models import Users, Posts, Follows, Likes
from werkzeug.utils import secure_filename
from flask_login import login_user, logout_user, current_user, login_required


###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('index.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html')
    
def requires_auth(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    auth = request.headers.get('Authorization', None)
    if not auth:
      return jsonify({'code': 'authorization_header_missing', 'description': 'Authorization header is expected'}), 401

    parts = auth.split()

    if parts[0].lower() != 'bearer':
      return jsonify({'code': 'invalid_header', 'description': 'Authorization header must start with Bearer'}), 401
    elif len(parts) == 1:
      return jsonify({'code': 'invalid_header', 'description': 'Token not found'}), 401
    elif len(parts) > 2:
      return jsonify({'code': 'invalid_header', 'description': 'Authorization header must be Bearer + \s + token'}), 401

    token = parts[1]
    try:
         payload = jwt.decode(token, token_key)
         get_user = Users.query.filter_by(id=payload['user_id']).first()

    except jwt.ExpiredSignature:
        return jsonify({'code': 'token_expired', 'description': 'token is expired'}), 401
    except jwt.DecodeError:
        return jsonify({'code': 'token_invalid_signature', 'description': 'Token signature is invalid'}), 401

    g.current_user = user = get_user
    return f(*args, **kwargs)

  return decorated

@app.route("/api/users/register", methods=["POST"]) 
def register():
    
    form = ProfileForm()
    
    if request.method == 'POST'and form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            firstname = form.firstname.data
            lastname = form.lastname.data
            email = form.email.data
            location = form.location.data
            bio = form.bio.data
            joined_on = datetime.date.today()
            
            photo = form.photo.data
            filename = secure_filename(photo.filename)
            photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            userid = generateUserId(firstname, lastname)
            
            user = Users(id=userid,password=password, firstname=firstname, lastname=lastname,
                      email= email,location= location, biography=bio, profile_photo=filename, joined_on=joined_on)
                
            db.session.add(user)
            db.session.commit()
            
            return jsonify(response=[{'message':'Successfully created account'}])
    error_retrieval = form_errors(form)
    error = [{'errors': error_retrieval}]
    return jsonify(errors=error)

@app.route("/api/auth/login", methods=["POST"])
def login():
    form = LoginForm()
    if request.method == "POST" and form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        
        user = Users.query.filter_by(username=username, password=password).first()
        if user is None:
            return jsonify(errors=[{'error':['Incorrect Username or Password.']}])
         
        login_user(user)  
        payload = {'user_id' : user.id}
        token = jwt.encode(payload, token_key)
        return jsonify(response=[{'message':'Log in successful','token': token, 'userid': user.id}])
    error_collection = form_errors(form)
    error = [{'errors': error_collection}]
    return jsonify(errors=error)
    
@app.route("/api/auth/logout", methods=["GET"])
@requires_auth
@login_required
def logout():
    if request.method == 'GET':
        logout_user()
    return jsonify(response=[{'message':'User successfully logged out.'}])

def convertposts(posts):
    liketest='';
    newposts=[]
    for i in range (0,len(posts)):
        user=Users.query.filter_by(id=posts[i].user_id).first();
        username=user.username;
        profilephoto=user.profile_photo;
        likevar=Likes.query.filter_by(post_id=posts[i].id,user_id=current_user.id).first()
        if likevar is None:
            liketest='No'
        else:
            liketest='Yes'
        x={
        'id':posts[i].id,
        'user_id':posts[i].user_id,
        'photo':"/static/uploads/"+posts[i].photo,
        'caption':posts[i].caption,
        'created_on':posts[i].created_on,
        'likes':countlikes(posts[i].id),
        'username':username,
        'userphoto':'/static/uploads/'+profilephoto,
        'likebyuser':liketest
        }
        newposts.append(x)
    return newposts

@app.route("/api/users/<user_id>/posts",methods=["GET","POST"])
@requires_auth
def addpost(user_id):
    
    form=PostForm()
    if request.method=="GET":
        thisuser=''
        if user_id==0 or user_id==current_user.id:
            uid=current_user.id
            thisuser='Yes'
            
        else:
            uid=user_id
            thisuser='No'
        user=Users.query.filter_by(id=uid).first()
        if user is not None:
            userinfo={'id':user.id,'username':user.username,'fname':user.first_name,'lname':user.last_name,'location':user.location,'photo':'/static/uploads/'+user.profile_photo,'bio':user.biography,'joined':user.joined_on}
            posts=Posts.query.filter_by(user_id=uid).all()
            follows=Follows.query.filter_by(user_id=uid).all()
            following=Follows.query.filter_by(follower_id=current_user.id, user_id=uid).first()
            isfollowing=''
            if following is None:
                isfollowing='No'
            else:
                isfollowing='Yes'
            return jsonify(response=[{'posts':[convertposts(posts)],'numposts':len(posts),'follows':len(follows),'userinfo':userinfo,'current':thisuser,'following':isfollowing}])
        else:
            return jsonify(error={'error':'User does not exist'});
    if request.method=="POST" and form.validate_on_submit():
        photo=form.photo.data
        filename=secure_filename(image.filename)
        created=datetime.datetime.now()
        post=Posts(current_user.id,filename,form.caption.data,created)
        db.session.add(post)
        db.session.commit()
        photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return jsonify(response=[{'message':'Post added successfully'}])
    return jsonify(errors=[{'error':form_errors(form)}])

@app.route("/api/posts",methods=["GET"])
@requires_auth
def getpost():
    posts=Posts.query.order_by(Posts.created_on).all()
    return jsonify(response=[{'posts':convertposts(posts)}])
    
@app.route("/api/posts/<post_id>/like",methods=["POST"])
@requires_auth
def likepost(post_id):
    if request.method=="POST":
        like=Likes(current_user.id,post_id)
        db.session.add(like)
        db.session.commit()
        count=countlikes(post_id)
        return jsonify(response=[{'message':'Post Liked'}])
        
def countlikes(post_id):
    count=Likes.query.filter_by(post_id=post_id).all()
    return len(count)

@app.route("/api/users/<user_id>/follow",methods=["POST"])
@requires_auth
def follow(user_id):
    if request.method=="POST":
        follow=Follows(user_id,current_user.id)
        db.session.add(follow)
        db.session.commit()
        user=Users.query.filter_by(id=user_id).first()
        return jsonify(response={'message':'You are now following '+user.username})

@login_manager.user_loader
def load_user(id):
    return Users.query.get(int(id))


def generateUserId(firstname, lastname):
    temp = re.sub('[.: -]', '', str(datetime.datetime.now()))
    temp = list(temp)
    temp.extend(list(map(ord,firstname)))
    temp.extend(list(map(ord,lastname)))
    random.shuffle(temp)
    temp = list(map(str,temp))
    return int("".join(temp[:7]))%10000000 

def form_errors(form):
    error_messages = []
    """Collects form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            message = u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                )
            error_messages.append(message)

    return error_messages

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
