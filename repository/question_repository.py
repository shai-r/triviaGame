from api.data_api import get_data
from models.Answer import Answer
from models.Question import Question
from repository.answer_repository import create_answer, delete_answer, delete_answer_by_question_id
from repository.database import get_db_connection, create_users_table
from typing import List, Optional

from repository.user_answer_repository import delete_user_answer_by_question_id


def create_question(question: Question) -> int:
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute("""
            INSERT INTO questions (question_text, correct_answer)
            VALUES (%s ,%s) RETURNING id
        """, (question.question_text, question.correct_answer))
        new_id = cursor.fetchone()['id']
        connection.commit()
        return new_id

def load_questions_and_answers_from_api():
    if get_all_questions() is None or len(get_all_questions()) < 20:
        data = get_data('https://opentdb.com/api.php?amount=20')
        questions = data['results']
        for q in questions:
            qid = create_question(Question(question_text=q['question'], correct_answer=q['correct_answer']))
            for a in q['incorrect_answers']:
                create_answer(Answer(question_id=qid, incorrect_answer=a))

def get_all_questions() -> List[Question]:
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute("SELECT * FROM questions")
        res = cursor.fetchall()
        questions = [Question(**q) for q in res]
        return questions if questions else None


def get_question_by_id(qid: int) -> Optional[Question]:
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute("SELECT * FROM questions WHERE id = %s", (qid,))
        question = cursor.fetchone()
        return None if not question else Question(**question)


def update_question(qid: int, question: Question) -> Question:
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute(
            "UPDATE questions SET question_text = %s, correct_answer = %s WHERE id = %s",
            (question.question_text, question.correct_answer, qid)
        )
        connection.commit()
        question = get_question_by_id(qid)
        return question

def delete_question(qid: int):
    delete_answer_by_question_id(qid)
    delete_user_answer_by_question_id(qid)
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute("DELETE FROM questions WHERE id = %s", (qid,))
        connection.commit()
        return get_question_by_id(qid) == None

