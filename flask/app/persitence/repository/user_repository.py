from app.persitence.models import User


def create_user(user):
    User(user).save()


def get_user_by_id(user_id):
    return User.find(_id=user_id).first_or_none()


def get_user_by_email(email):
    print('*'*80, 'hehe','*'*80, '\n', User.collection.database.client.server_info(), '\n', '*'*80, flush=True)
    return User.find(email=email).first_or_none()


def get_user_by_full_name(name):
    return User.find(full_name=name).first_or_none()


def get_all_users():
    return User.all()

def get_all_users_with_name_starting_with(pattern):
    return User.find(full_name=f'/^{pattern}/')
