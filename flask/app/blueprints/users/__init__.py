import os

from werkzeug.utils import secure_filename
from bson import ObjectId
from flask import Blueprint, redirect, url_for, render_template, request, current_app
from flask_login import logout_user, login_required, current_user

from app.controllers.message_controller import create_message, get_all_messages_for_user, get_message_by_id
from app.controllers.user_controller import set_avatar_color

bp_user = Blueprint('bp_user', __name__)


@bp_user.before_request
def before_request():
    if not current_user.is_authenticated or not current_user.has_access('user'):
        return redirect(url_for('bp_open.index'))

@bp_user.get('/signout')
def signout_get():
    logout_user()
    return redirect(url_for('bp_open.index'))


@bp_user.get('/profile')
def profile_get():
    if current_user.avatar.startswith('http'):
        background_color = current_user.avatar.split('background=')[1][:6]
        color = current_user.avatar.split('color=')[1][:6]
    else:
        background_color = '000000'
        color = 'ffffff'

    return render_template('profile.html', background_color=background_color, color=color)


@bp_user.get('/message')
def message_get():
    messages = get_all_messages_for_user()
    return render_template('message.html', messages=messages)


@bp_user.post('/message')
def message_post():
    to = request.form['to']
    message = request.form['message']
    create_message(to, message)
    return redirect(url_for('bp_user.message_get'))


@bp_user.get('/read_message/<message_id>')
def read_message(message_id):
    message = get_message_by_id(ObjectId(message_id))

    message.message_body = message.message_body.replace('\n', '<br />')
    return render_template('single_message.html', message=message)


@bp_user.post('/avatar/color')
def avatar_color_post():
    background_color = request.form['background_color']
    color = request.form['color']
    set_avatar_color(background_color[1:], color[1:])
    return redirect(url_for('bp_user.profile_get'))


@bp_user.post('/avatar/upload')
def upload_avatar_post():
    photo = request.files.get('photo', None)
    if photo is not None:
        filename = secure_filename(photo.filename)
        _, extension = os.path.splitext(filename)

        avatar_filename = current_app.config['AVATAR_FOLDER'] + str(current_user._id) + extension
        path = current_app.config['AVATAR_FOLDER_BASE'] + avatar_filename
        photo.save(path)
        current_user.avatar = avatar_filename
        current_user.save()
    return redirect(url_for('bp_user.profile_get'))
