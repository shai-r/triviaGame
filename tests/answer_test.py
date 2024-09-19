import pytest
from repository.database import create_all_tables, drop_all_tables
from repository.answer_repository import *
from repository.question_repository import load_questions_and_answers_from_api


@pytest.fixture(scope="module")
def setup_database():
    create_all_tables()
    load_questions_and_answers_from_api()
    yield
    drop_all_tables()

def test_create_answer(setup_database):
    new_id = create_answer(Answer(question_id=1, incorrect_answer="bla!!!"))
    assert new_id >=21

def test_get_all_answers(setup_database):
    answers = get_all_answers()
    assert answers

def test_get_answer_by_id(setup_database):
    answer = get_answer_by_id(3)
    assert answer.id == 3

def test_get_answers_by_question_id(setup_database):
    answers = get_all_answers_by_question_id(1)
    assert len(answers) > 1

def test_update_answer(setup_database):
    update_answer(3, Answer(question_id=15, incorrect_answer="bla!!!"))
    answer = get_answer_by_id(3)
    assert answer.incorrect_answer=="bla!!!"

def test_delete_answer(setup_database):
    assert delete_answer(3)

def test_delete_answer_by_question_id(setup_database):
    assert delete_answer_by_question_id(1)
