from functools import wraps

from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user

bp_admin = Blueprint('bp_admin', __name__)


def require_access_level(level):
    def decorator(route_func):
        @wraps(route_func)
        def wrapper(*args, **kwargs):
            if current_user.is_authenticated:
                if current_user.has_access(level):
                    return route_func(*args, **kwargs)
            return redirect(url_for('bp_open.index'))
        return wrapper
    return decorator


@bp_admin.before_request
def before_request():
    if not current_user.is_authenticated or not current_user.has_access('admin'):
        return redirect(url_for('bp_open.index'))


@bp_admin.get('/admin')
#@require_access_level('admin')
def admin_get():
    return render_template('admin.html')