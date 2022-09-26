from operator import and_
from flask.globals import session
from flask.templating import DispatchingJinjaLoader
from sqlalchemy import engine
from sqlalchemy.engine import url
from website import DB_NAME
from flask import Blueprint, app, render_template, request, flash, redirect, url_for
from .models import Donate, User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db    
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy import and_, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

auth = Blueprint('auth', __name__)

@auth.route('/')
def home():
   return render_template("index.html")



@auth.route('/login.html', methods=[ 'GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('user')
        password = request.form.get('pass')

        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in Successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('auth.home'))
            else:
                flash('Incorrect password, try again!', category='error')
        else:
            flash('Username does not exist!', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/sign-up.html', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('user')
        password = request.form.get('pass')
        rpassword = request.form.get('rpass')

        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already exists', category='error')
        elif password != rpassword:
            flash('Passwords do not match', category='error')
        elif username == password:
            flash('Username and Password cannot be the same', category='error')
        else:
            new_user = User(username=username, password=generate_password_hash(password, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('Account created!', category='success')
            return redirect(url_for('auth.login'))
    return render_template("sign-up.html", user=current_user)


@auth.route('/search.html', methods=['POST', 'GET'])
@login_required
def search():
    if request.method == 'POST':
       blood_group = request.form.get('blood_group')
       district = request.form.get('district')
       results = Donate.query.filter(and_(Donate.blood_group==blood_group, Donate.district==district))

       return render_template("results.html", results = results)
       
    return render_template("search.html")

@auth.route('/register.html', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
       name = request.form.get('name')
       blood_group = request.form.get('blood_group')
       district = request.form.get('district')
       mob_no = request.form.get('mob_no')
       quantity = 1
       new_donate = Donate(name=name, blood_group=blood_group, district=district, mob_no=mob_no, quantity=quantity)
       db.session.add(new_donate)
       db.session.commit()
       flash('Successfully registered as Donar', category='success')
       return redirect(url_for('auth.home'))
    
    return render_template("register.html", user=current_user)

@auth.route('/register-org.html', methods=['GET', 'POST'])
def register_org():
    if request.method == 'POST':
       name = request.form.get('name')
       blood_group = request.form.get('blood_group')
       quantity = request.form.get('quantity')
       district = request.form.get('district')
       mob_no = request.form.get('mob_no')
       new_donate = Donate(name=name, blood_group=blood_group, quantity=quantity, district=district, mob_no=mob_no)
       db.session.add(new_donate)
       db.session.commit()
       flash('Successfully registered as an Organization', category='success')
       return redirect(url_for('auth.home'))
    
    return render_template("register-org.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    flash("Logged out Successfully!")
    logout_user()
    return redirect(url_for('auth.home'))


@auth.route('/results.html')
@login_required
def results():
    return render_template("results.html", user=current_user)


