import dotenv
from flask import Flask
from flask_login import LoginManager
import dotenv



def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('settings.py')

    from app.persitence.db import init_db
    init_db(app)

    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_email):
        from app.controllers.user_controller import get_user_by_email
        return get_user_by_email(user_email)

    from app.blueprints.open import bp_open
    app.register_blueprint(bp_open)

    from app.blueprints.users import bp_user
    app.register_blueprint(bp_user)

    from app.blueprints.admin import bp_admin
    app.register_blueprint(bp_admin)

    from app.blueprints.ajax import bp_ajax
    app.register_blueprint(bp_ajax, url_prefix='/ajax')

    return app

dotenv.load_dotenv()
app = create_app()
