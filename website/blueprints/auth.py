from flask import Blueprint, redirect, render_template, request, url_for, flash
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import current_user, login_required, login_user, logout_user
from website.models import User

from website.token import generate_confirmation_token, confirm_token
from website.email import send_email

from website import db
import datetime

auth = Blueprint('auth', __name__)


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))

    if request.method == 'POST':
        f_name = request.form.get('f_name')
        l_name = request.form.get('l_name')
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()

        if user:
            flash('User already exists', category='login_error')
        elif len(email) < 5:
            flash('Email must be greater than 4 characters',
                  category='login_error')
        elif len(f_name) < 1:
            flash('First name must be greater than 1 character',
                  category='login_error')
        elif len(l_name) < 1:
            flash('Last name must be greater than 1 character',
                  category='login_error')
        elif len(password1) < 7:
            flash('Last name must be at least 8 characters long',
                  category='login_error')
        elif password1 != password2:
            flash('Passwords must match',
                  category='login_error')
        else:
            new_user = User(f_name=f_name, l_name=l_name, email=email,
                            password=generate_password_hash(password1, method='sha256'), confirmed=False)
            db.session.add(new_user)
            db.session.commit()

            token = generate_confirmation_token(new_user.email)
            confirm_url = url_for('auth.confirm_email', token=token, _external=True)
            html = render_template('confirmemail.html', confirm_url=confirm_url)
            subject = 'Please confirm your email'
            send_email(new_user.email, subject, html)

            flash('Account created! Please confirm your email',
                  category='login_success')

    return render_template('auth/sign-up.html', user=current_user)


@auth.route('/confirm/<token>')
def confirm_email(token):
    try:
        email = confirm_token(token)
    except:
        flash('The confirmation link is invalid or expired',
              category='login_error')

    user = User.query.filter_by(email=email).first_or_404()
    if user.confirmed:
        flash('Account already confirmed. Please login', category='login_success')
    else:
        user.confirmed = True
        user.confirmed_on = datetime.datetime.now()
        db.session.commit()
        flash('You have confirmed your account. Thanks!', 'login_success')
    return redirect(url_for('auth.login'))


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user:
            if check_password_hash(user.password, password):
                login_user(user)
                flash('Logged in correctly!', category='login_success')
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, please try again.',
                      category='login_error')
        else:
            flash('Email doesn\'t exist')

    return render_template('auth/login.html', user=current_user)


@auth.route('/logout')
def logout():
    logout_user()
    flash('Logged out succesfully!', category='login_success')
    return redirect(url_for('auth.login'))
