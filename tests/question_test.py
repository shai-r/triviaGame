import pytest
from repository.database import create_all_tables, drop_all_tables
from repository.question_repository import *
from models.User import User

@pytest.fixture(scope="module")
def setup_database():
    create_all_tables()
    load_questions_and_answers_from_api()
    yield
    drop_all_tables()

def test_create_question(setup_database):
    new_id = create_question(Question(question_text="what??", correct_answer="yes!!!"))
    assert new_id == 21

def test_get_all_questions(setup_database):
    questions = get_all_questions()
    assert questions

def test_get_question_by_id(setup_database):
    question = get_question_by_id(3)
    assert question.id == 3

def test_update_question(setup_database):
    update_question(3, Question(question_text="what??", correct_answer="yes!!!"))
    question = get_question_by_id(3)
    assert question.question_text == 'what??'

def test_delete_question(setup_database):
    assert delete_question(3)
