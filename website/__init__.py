from flask import Flask 

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hefuqwhegwqeg'
    app.config['SESSION_COOKIE_NAME'] = 'something'
    
    from .views import views 

    app.register_blueprint(views)

    return app


