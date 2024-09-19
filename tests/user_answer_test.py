from datetime import timedelta
import pytest
from repository.database import create_all_tables, drop_all_tables
from repository.question_repository import load_questions_and_answers_from_api
from repository.user_answer_repository import *
from repository.user_repository import load_users_from_api

@pytest.fixture(scope="module")
def setup_database():
    create_all_tables()
    load_users_from_api()
    load_questions_and_answers_from_api()
    yield
    drop_all_tables()

def create():
    create_user_answer(
        UserAnswer(
            user_id=1,
            question_id=1,
            answer_text="yes!!!",
            is_correct=True,
            time_taken=timedelta(milliseconds=10000)
        )
    )
    create_user_answer(
        UserAnswer(
            user_id=2,
            question_id=1,
            answer_text="yews!!!",
            is_correct=True,
            time_taken=timedelta(milliseconds=100000)
        )
    )

def test_create_user_answer(setup_database):
    new_id = create_user_answer(
        UserAnswer(
            user_id=1,
            question_id=1,
            answer_text="yes!!!",
            is_correct=True,
            time_taken=timedelta(milliseconds=10000)
        )
    )
    assert new_id >= 1

def test_get_all_user_answers(setup_database):
    create()
    user_answer = get_all_user_answers()
    assert user_answer

def test_get_user_answer_by_id(setup_database):
    create()
    user_answer = get_user_answer_by_id(1)
    assert user_answer.id == 1

def test_get_all_user_answers_by_user_id(setup_database):
    create()
    user_answer = get_all_user_answers_by_user_id(1)
    assert user_answer

def test_get_all_user_answers_by_question_id(setup_database):
    create()
    user_answer = get_all_user_answers_by_question_id(1)
    assert user_answer

def test_get_all_user_answers_by_correct_answer(setup_database):
    create()
    user_answer = get_all_user_answers_by_correct_answer(True)
    assert user_answer and all(map(lambda ua: ua.is_correct == True, user_answer))

def test_update_user_answer(setup_database):
    create()
    update_user_answer(
        1, UserAnswer(
            user_id=2,
            question_id=2,
            answer_text="no!!!",
            is_correct=False,
            time_taken=timedelta(milliseconds=1000)
        )
    )
    user_answer = get_user_answer_by_id(1)
    assert user_answer.answer_text == 'no!!!'

def test_delete_user_answer(setup_database):
    create()
    assert delete_user_answer(1)

def test_delete_user_answer_by_user_id(setup_database):
    create()
    assert delete_user_answer_by_user_id(1)

def test_delete_user_answer_by_question_id(setup_database):
    create()
    assert delete_user_answer_by_question_id(1)