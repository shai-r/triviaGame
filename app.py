from flask import Flask

from controllers.questions_controller import questions_blueprint
from controllers.user_controller import *
from repository.database import create_all_tables
from repository.question_repository import load_questions_and_answers_from_api
from repository.user_repository import  load_users_from_api

app = Flask(__name__)

if __name__ == '__main__':
    create_all_tables()
    load_users_from_api()
    load_questions_and_answers_from_api()
    app.register_blueprint(user_blueprint, url_prefix="/api/users")
    app.register_blueprint(questions_blueprint, url_prefix="/api/questions")
    app.run(debug=True)