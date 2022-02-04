import datetime
import random

from passlib.hash import argon2
from flask_login import login_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.persitence.repository import user_repository


def create_user(first_name, last_name, email, password):
    background, color = generate_random_avatar_color()
    user = {
        'first_name': first_name,
        'last_name': last_name,
        'full_name': f'{first_name} {last_name}',
        'email': email,
        'password': argon2.using(rounds=12).hash(password),
        'access_level': 'user',
        'date_created': datetime.datetime.now(),
        'last_signin': None,
        'status': 'offline',
        'activated': False,
        'avatar': f'https://eu.ui-avatars.com/api/?name={first_name}+{last_name}&background={background}&color={color}',
        'address': {
            'address_line_1': None,
            'address_line_2': None,
            'zip': None,
            'state': None,
            'country': None
        },

        'courses': [],
        'settings': None,
        'social_profiles': None
    }

    user_repository.create_user(user)


def get_user_by_email(email):
    return user_repository.get_user_by_email(email)


def verify_user(email, password):
    user = user_repository.get_user_by_email(email)
    if user is None:
        return False
    if user.password.startswith('pbkdf2:sha256'):
        verified = check_password_hash(user.password, password)
        if verified:
            user.password = argon2.using(rounds=12).hash(password)
            user.save()
        return verified
    return argon2.verify(password, user.password)


def signin_user(email):
    user = get_user_by_email(email)
    if user is not None:
        login_user(user)
        user.last_signin = datetime.datetime.now()
        user.save()


def get_user_by_full_name(name):
    return user_repository.get_user_by_full_name(name)


def get_all_users_with_name_starting_with(pattern):
    result_list = user_repository.get_all_users()

    return [user.full_name for user in result_list if user.full_name.lower().startswith(pattern)]


def generate_random_avatar_color():
    default_colors = [
        {
            'background': '0D8ABC',
            'color': 'ffffff'
        },
        {
            'background': 'CD8ABC',
            'color': 'dddddd'
        },
        {
            'background': '1AC1F2',
            'color': '3C1ABD'
        },
        {
            'background': '1A0315',
            'color': '03FF03'
        }
    ]
    color = random.choice(default_colors)
    return color['background'], color['color']


def set_avatar_color(background_color=None, color=None):
    user = current_user
    back, front = generate_random_avatar_color()
    if background_color is None:
        background_color = back
    if color is None:
        color = front

    user.avatar = f'https://eu.ui-avatars.com/api/?name={user.first_name}+{user.last_name}&background={background_color}&color={color}'
    user.save()
