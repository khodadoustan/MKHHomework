from flask_login import LoginManager

from auth import auth_app
from init import create_app
from main import shortlink_app
from models import User

app = create_app()

app.register_blueprint(shortlink_app)
app.register_blueprint(auth_app)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return User.query.get(int(user_id))


if __name__ == '__main__':
    app.run()
