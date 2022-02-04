import json

from flask import Blueprint, request
from flask_cors import CORS, cross_origin

from app.controllers.message_controller import get_new_msg_count_for_user
from app.controllers.user_controller import get_all_users_with_name_starting_with

bp_ajax = Blueprint('bp_ajax', __name__)

cors = CORS(bp_ajax)


@bp_ajax.post('/all_users')
@cross_origin()
def all_users_post():
    result = request.get_json()
    value = result['value'].lower()
    result_list = get_all_users_with_name_starting_with(value)
    return json.dumps(result_list)


@bp_ajax.get('/check_msg')
@cross_origin()
def check_msg_get():
    user_id = request.cookies.get('user_id')

    msg_count = get_new_msg_count_for_user(user_id)

    result = {
        'unread_msg_count': msg_count
    }

    return json.dumps(result)
