from app import app
from app.models import User
from flask_login import current_user, login_user, logout_user, login_required
from flask import render_template, flash, redirect, get_flashed_messages, url_for, request
from app.forms import LoginForm
from werkzeug.urls import url_parse

@app.route('/')
@app.route('/index')
#@login_required
def index():
    posts = [
            
            {
                'author': {'username': 'Pete'},
                'body': 'The Nigerian Condition',
                'rank': '1'
                },
            {
                'author': {'username': 'John'},
                'body': 'My Experience Travelling Nigeria',
                'rank': '2'

                },
            {
                'author':{'username': 'Don'},
                'body': 'How To Use Google Properly',
                'rank': '3'
                }

            ]
    return render_template('index.html', posts=posts)

@app.route('/register')
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    # Create a RgistrationForm object
    form = RegistrationForm()

    # if form.validate_on_submit():
        

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Check if a user is already logged in redirect to homepage
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    # Create a LoginForm object
    form = LoginForm()
    
    # Check if form validates
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', form= form, title='Sign In')
    

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('index'))
