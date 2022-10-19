from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from website.models import User
from website import db

settings = Blueprint('settings', __name__)

@settings.route('/settings')
@login_required
def home():
    pass

@settings.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if request.method == 'POST':
        f_name = request.form.get('f_name')
        l_name = request.form.get('l_name')

        user = User.query.filter_by(id=current_user.id).first()

        user.f_name = f_name
        user.l_name = l_name

        db.session.commit()

    return render_template('settings/editprofile.html', user=current_user)