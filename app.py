import os
import uuid as uuid
from werkzeug.utils import secure_filename
from datetime import date, datetime
from unicodedata import category

from flask import Flask, flash, redirect, render_template, request, url_for, session
from flask_ckeditor import CKEditor, CKEditorField
from flask_login import (LoginManager, UserMixin, current_user, login_required,
                         login_user, logout_user)
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

from form import AddPostForm, LoginForm, UserForm , roleForm, ContactForm , editProfileForm , forgotPassword ,resetPassword

app = Flask(__name__)
ckeditor = CKEditor(app)

UPLOAD_FOLDER = 'static/images/profile_pic'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

UPLOAD_FOLDER2 = 'static/images/feature_photo'
app.config['UPLOAD_FOLDER2'] = UPLOAD_FOLDER2

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
# Add DataBase mysql
# app.config['SQLALCHEMY_DATABASE_URI']='mysql://username:password@localhost/db_name'
# app.config['SQLALCHEMY_DATABASE_URI']='mysql://rahul:password123@localhost/users'
app.config['SECRET_KEY'] = "secret key"
db = SQLAlchemy(app)
migrate = Migrate(app, db)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


# Create a String
def __repr__(self):
    return '<Name %r>' % self.name


@app.route("/")
def index():
    return redirect(url_for('home'))


################################################################################

#aboute page

@app.route("/about")
def about():
    return render_template('about.html')


################################################################################

#authors page

@app.route("/authors")
def authors():
    return render_template('authors.html')

################################################################################

#home page

@app.route("/home")
def home():

    # all_like=[]
    # all_posts = Posts.query.all()
    # for post in all_posts:
    #     for like in post.likes:
    #         all_like.append(like.liker_id)
    # print(all_like)
    

    #uttarakhand posts
    historyPosts = Posts.query.filter_by(category='Uttarakhand History').order_by(Posts.date_time.desc()).limit(5).all()
    geographyPosts = Posts.query.filter_by(category='Uttarakhand Geography').order_by(Posts.date_time.desc()).limit(5).all()
    currentPosts = Posts.query.filter_by(category='Uttarakhand Current').order_by(Posts.date_time.desc()).limit(5).all()

    #India posts
    IndhistoryPosts = Posts.query.filter_by(category='India History').order_by(Posts.date_time.desc()).limit(5).all()
    IndgeographyPosts = Posts.query.filter_by(category='India Geography').order_by(Posts.date_time.desc()).limit(5).all()
    IndcurrentsPosts = Posts.query.filter_by(category='India Current').order_by(Posts.date_time.desc()).limit(5).all()

    return render_template('home.html', historyPosts=historyPosts, geographyPosts=geographyPosts, currentPosts=currentPosts, IndhistoryPosts=IndhistoryPosts, IndgeographyPosts=IndgeographyPosts, IndcurrentsPosts=IndcurrentsPosts)


################################################################################

#add post

@app.route("/addpost", methods=['GET', 'POST'])
def addpost():
    form = AddPostForm()
    if form.validate_on_submit():
        title = form.title.data
        category = form.category.data
        content = form.content.data
        poster = current_user.id
        if request.files['image']:
            image = request.files['image']
            filename = secure_filename(image.filename)
            image_name = str(uuid.uuid1()) + "_" + filename
            image.save(os.path.join(app.config['UPLOAD_FOLDER2'], image_name))
            
        else:
            image_name = 'default.jpg'
        post = Posts(title=title, category=category, content=content, poster_id=poster, image=image_name)
        db.session.add(post)
        db.session.commit()
        flash('Post Added Successfully', 'success')
        return redirect(url_for('dashboard'))
    else:
        print(form.errors)
    return render_template('addpost.html', form=form)
    


    
    # if request.files['profile_pic']:
    #         pic = request.files['profile_pic']
    #         filename = secure_filename(pic.filename)
    #         pic_name = str(uuid.uuid1()) + "_" + filename
    #         pic.save(os.path.join(app.config['UPLOAD_FOLDER'], pic_name))
    #         user.profile_pic = pic_name
          


################################################################################

#edit post

@app.route('/edit_post/<int:id>',methods=['GET','POST'])
@login_required
def edit_post(id):
    post = Posts.query.get(id)
    form = AddPostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.category = form.category.data
        post.content = form.content.data
        if request.files['image']:
            image = request.files['image']
            filename = secure_filename(image.filename)
            image_name = str(uuid.uuid1()) + "_" + filename
            image.save(os.path.join(app.config['UPLOAD_FOLDER2'], image_name))
            post.image = image_name
        
            

        db.session.commit()
        flash('Post updated successfully',category='success')
        return redirect(url_for('home'))
    elif request.method == 'GET':
        form.title.data = post.title
        form.category.data = post.category
        form.content.data = post.content
    return render_template('edit_post.html',form=form,post=post)

################################################################################

#register

@app.route("/register", methods=['GET', 'POST'])
def register():
    name = None
    form = UserForm()
    # validate form
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            # Hash Password
            if form.password_hash.data == form.password_hash2.data:
                password_hash = generate_password_hash(form.password_hash.data, "sha256")
                user = Users(name=form.name.data, email=form.email.data, username=form.username.data,about_author=form.about_author.data, password_hash=password_hash,phone=form.phone.data,security_question=form.security_question.data,security_answer=form.security_answer.data)
                db.session.add(user)
                db.session.commit()
                flash('User registered successfully')
                name = form.name.data
                form.name.data = ""
                form.username.data = ""
                form.email.data = ""
                form.about_author.data = ""
                form.password_hash.data = ""
                flash("User Added Successfully")
                return redirect(url_for('home'))
            else:
                flash('Password does not match')
                return redirect(url_for('register'))
    else:
        print(form.errors)
    return render_template('register.html', form=form, name=name)


################################################################################

#login

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password_hash, form.password.data):
                if user.role == 'Admin':
                    role = 'Admin'
                    login_user(user)
                    return redirect(url_for('home',role=role))
                
                if user.role == 'Author':
                    role='Author'
                    login_user(user)
                    return redirect(url_for('home',role=role))
                
                if user.role == 'User':
                    role='User'
                    login_user(user)
                    return redirect(url_for('home',role=role))

                    
                else:
                    print(user.role)
                    flash("User not found")
                
        else:
            flash("That user dosent exists! Try Again!")
            print(form.errors)
    return render_template('login.html', form=form)


################################################################################

#logout

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash("You have been logged out")
    return redirect(url_for('login'))


################################################################################

#dashboard

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    post = Posts.query.filter_by(poster_id=current_user.id).all()

    total_posts=Posts.query.filter_by(poster_id=current_user.id).count()

    total_views = 0
    for p in post:
        for v in p.views:
            total_views += v.view_count

    total_likes = 0
    for p in post:
        for l in p.likes:
            total_likes += 1

    return render_template('dashboard.html',post=post,total_posts=total_posts,total_views=total_views,total_likes=total_likes)


################################################################################

#all users

@app.route('/admin_all_users', methods=['GET', 'POST'])
@login_required
def admin_all_users():
    users = Users.query.all()
    return render_template('admin_all_users.html',users=users)

################################################################################





#admin messages

@app.route('/admin_messages', methods=['GET', 'POST'])
@login_required
def admin_messages():
    messages = Contact.query.all()
    return render_template('admin_messages.html',messages=messages)


##############################################################################



#all_posts

@app.route('/admin_all_posts', methods=['GET', 'POST'])
@login_required
def admin_all_posts():
    posts = Posts.query.all()
    return render_template('admin_all_posts.html',posts=posts)


################################################################################


#your posts


@app.route('/your_posts', methods=['GET', 'POST'])
@login_required
def your_posts():
    posts = Posts.query.filter_by(poster_id=current_user.id).all()
    return render_template('your_posts.html',posts=posts)




# #adming page

# @app.route('/admin', methods=['GET', 'POST'])
# @login_required
# def admin():
#     id = current_user.id
#     if id == 1 or current_user.role == 'Admin':
#         users = Users.query.all()
#         posts = Posts.query.all()
#         msg = Contact.query.all()
#         return render_template('admin.html', users=users, posts=posts, msg=msg)
#     else:
#         flash("You are not admin")
#         return redirect(url_for('home'))


# ################################################################################

#delete post

@app.route('/posts/delete/<int:id>')
@login_required
def delete_post(id):
    post_to_delete = Posts.query.get_or_404(id)
    likes = Likes.query.filter_by(post_id=id).all()
    views = Views.query.filter_by(post_id=id).all()
    try:
        for like in likes:
            db.session.delete(like)
            db.session.commit()
        for view in views:
            db.session.delete(view)
            db.session.commit()

        db.session.delete(post_to_delete)
        db.session.commit()
        return redirect('/dashboard')
    except:
        flash("There was a problem deleting that post")
        return redirect('/dashboard')


################################################################################

#admin edit user

@app.route('/admin_edit_user/<int:id>', methods=['GET', 'POST'])
@login_required
def admin_edit_user(id):
    form = roleForm()
    name_to_edit = Users.query.get_or_404(id)
    if request.method == 'POST':
        name_to_edit.role = form.role.data
        try:
            db.session.commit()
            return redirect('/dashboard')
        except:
            flash("There was a problem editing that user")
            return render_template('admin_edit_user.html', form=form, name_to_edit=name_to_edit, id=id)
    else:
        return render_template('admin_edit_user.html', form=form, name_to_edit=name_to_edit, id=id)


################################################################################

#admin delete user

@app.route('/admin_delete_user/<int:id>',methods=['GET','POST'])
@login_required
def admin_delete_user(id):
    user_to_delete = Users.query.get_or_404(id)
    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        return redirect('/dashboard')
    except:
        flash("There was a problem deleting that user")
        return redirect('/dashboard')


################################################################################

#conatct 

@app.route("/contact", methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        name = form.yourname.data
        email = form.youremail.data
        subject = form.subject.data
        message = form.message.data
        msg = Contact(name=name, email=email, subject=subject, message=message)
        print(msg)
        db.session.add(msg)
        db.session.commit()
        flash('Message Send successfully')
        return redirect(url_for('home'))
    else:
        print(form.errors)

    return render_template('contact.html', form=form)


################################################################################

#edit profile

@app.route("/edit_profile/<int:id>",methods=['GET','POST'])
def edit_profile(id):
    form=editProfileForm()
    user = Users.query.get(id)
    if request.method == 'POST':
        user.name= form.name.data
        user.about_author= form.about_author.data
        if request.files['profile_pic']:
            pic = request.files['profile_pic']
            filename = secure_filename(pic.filename)
            pic_name = str(uuid.uuid1()) + "_" + filename
            pic.save(os.path.join(app.config['UPLOAD_FOLDER'], pic_name))
            user.profile_pic = pic_name
          
    
        try:
            db.session.commit()
            return redirect(url_for('dashboard'))
        except:
            flash("There was a problem editing that user")
            return render_template('edit_profile.html', form=form, user=user)
    else:
        return render_template('edit_profile.html', form=form, user=user)



################################################################################

#all post

@app.route("/allposts/<string:category>", methods=['GET', 'POST'])
def allposts(category):
    posts = Posts.query.filter_by(category=category).all()
    posts.reverse()
    
    return render_template('allposts.html', posts=posts)


################################################################################

#postpage

@app.route("/postpage/<int:id>")
def postpage(id):



    all_like=[]
    posts = Posts.query.filter_by(id=id).first()
    # like=Likes.query.filter_by(post_id=id).all()
    like=Likes.query.filter_by(post_id=id).all()
    for i in like:
        all_like.append(i.liker_id)



    # count views
    views = Views.query.filter_by(post_id=id).first()
    if views:
        views.view_count += 1
        db.session.commit()
    else:
        views = Views(post_id=id, view_count=1)
        db.session.add(views)
        db.session.commit()

    # views
    views = Views.query.filter_by(post_id=id).first()
    view_count = views.view_count

    return render_template('postpage.html',posts=posts,all_like=all_like,view_count=view_count)


################################################################################

#Likes  

@app.route('/like/<int:id>', methods=["GET","POST"])
@login_required
def like(id):

    post=Posts.query.filter_by(id=id).first()
    like=Likes.query.filter_by(liker_id=current_user.id,post_id=post.id).first()
    if like:
        db.session.delete(like)
        db.session.commit()
        return redirect(url_for('postpage',id=post.id))
    else:
        new_like=Likes(liker_id=current_user.id,post_id=post.id)
        db.session.add(new_like)
        db.session.commit()
        return redirect(url_for('postpage',id=post.id))


################################################################################

#forgot password

@app.route('/forgotpassword',methods=['GET','POST'])
def forgotpassword():
    form = forgotPassword()
    if form.validate_on_submit():
        email = form.email.data
        user = Users.query.filter_by(email=email).first()
        if user:
            form=resetPassword()
            email=user.email
            security_answer=user.security_answer
            security_question=user.security_question
            session['email']=email
            session['security_answer']=security_answer
            session['security_question']=security_question
            return redirect(url_for('resetpassword',email=email,security_answer=security_answer,security_question=security_question))
        else:
            flash("Email not found",category='danger')
            return redirect(url_for('forgotpassword'))
    else:
        print(form.errors)
    return render_template('forgotpassword.html',form=form)


################################################################################

# resetPassword with security security_question

@app.route('/resetpassword',methods=['GET','POST'])
def resetpassword():
    form=resetPassword()
    if form.validate_on_submit():
        email=session.get('email')
        security_answer=session.get('security_answer')
        security_question=session.get('security_question')
        print(email)
        print(security_answer)
        print(security_question)
        if security_question==form.security_question.data and security_answer==form.security_answer.data:
            user=Users.query.filter_by(email=email).first()
            new_password=form.password_hash.data
            user.password_hash=generate_password_hash(new_password,method='sha256')
            db.session.commit()
            flash("Password reset successful",category='success')
            session.pop('email',None)
            session.pop('security_answer',None)
            session.pop('security_question',None)
            return redirect(url_for('login'))
        else:
            flash("Wrong security question or password",category='danger')
            return redirect(url_for('resetpassword'))
    else:
        print(form.errors)
    return render_template('resetpassword.html',form=form)
    

################################################################################


#Likes from homepage 

# @app.route('/likehomepage/<int:id>', methods=["GET","POST"])
# @login_required
# def likehomepage(id):

#     post=Posts.query.filter_by(id=id).first()
#     like=Likes.query.filter_by(liker_id=current_user.id,post_id=post.id).first()
#     if like:
#         db.session.delete(like)
#         db.session.commit()
#         return redirect(url_for('home'))
#     else:
#         new_like=Likes(liker_id=current_user.id,post_id=post.id)
#         db.session.add(new_like)
#         db.session.commit()
#         return redirect(url_for('home'))


################################################################################






############################  DATABASES  ########################################

#post database

class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    content = db.Column(db.String(500), nullable=False)
    date_added = db.Column(db.Date, default=date.today)
    date_time = db.Column(db.DateTime, default=datetime.utcnow)
    poster_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    likes=db.relationship('Likes',backref='post',passive_deletes=True)
    views=db.relationship('Views',backref='post',passive_deletes=True)
    image = db.Column(db.String(), nullable=True)

# ---------------------------------------------------------------------------------------

#user database

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    phone = db.Column(db.String(50), nullable=False)
    date_added = db.Column(db.Date, default=date.today)
    about_author = db.Column(db.String(500), nullable=False)
    security_question = db.Column(db.String(50), nullable=False)
    security_answer = db.Column(db.String(50), nullable=False)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(10), default='User')
    posts = db.relationship('Posts', backref='poster')
    likes=db.relationship('Likes',backref='user',passive_deletes=True)
    profile_pic=db.Column(db.String(), nullable=True)

# ---------------------------------------------------------------------------------------

#contact database

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    subject = db.Column(db.String(50), nullable=False)
    message = db.Column(db.String(500), nullable=False)
    date_added = db.Column(db.Date, default=date.today)

# ---------------------------------------------------------------------------------------

#likes database

class Likes(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    date_liked=db.Column(db.DateTime, default=datetime.utcnow)
    liker_id=db.Column(db.Integer,db.ForeignKey('users.id'),nullable=True)
    post_id=db.Column(db.Integer,db.ForeignKey('posts.id'),nullable=True)
    



class Views(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    date_viewed=db.Column(db.DateTime, default=datetime.utcnow)
    view_count = db.Column(db.Integer, default=0)
    post_id=db.Column(db.Integer,db.ForeignKey('posts.id'),nullable=True)




if __name__ == "__main__":
    app.run(debug=True)
