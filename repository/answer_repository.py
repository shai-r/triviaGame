from models.Answer import Answer
from repository.database import get_db_connection, create_users_table
from typing import List, Optional

def create_answer(answer: Answer) -> int:
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute("""
            INSERT INTO answers (question_id, incorrect_answer)
            VALUES (%s, %s) RETURNING id
        """, (answer.question_id, answer.incorrect_answer))
        new_id = cursor.fetchone()['id']
        connection.commit()
        return new_id

def get_all_answers() -> List[Answer]:
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute("SELECT * FROM answers")
        res = cursor.fetchall()
        answers = [Answer(**a) for a in res]
        return answers if len(answers) > 0 else None


def get_answer_by_id(aid: int) -> Optional[Answer]:
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute("SELECT * FROM answers WHERE id = %s", (aid,))
        answer = cursor.fetchone()
        return None if not answer else Answer(**answer)

def get_all_answers_by_question_id(qid: int) -> Optional[Answer]:
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute("SELECT * FROM answers WHERE question_id = %s", (qid,))
        res = cursor.fetchall()
        answers = [Answer(**a) for a in res]
        return answers if len(answers) > 0 else None

def update_answer(aid: int, answer: Answer) -> Answer:
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute(
            "UPDATE answers SET question_id = %s, incorrect_answer = %s WHERE id = %s",
            (answer.question_id, answer.incorrect_answer, aid)
        )
        connection.commit()
        answer = get_answer_by_id(aid)
        return answer

def delete_answer(aid: int):
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute("DELETE FROM answers WHERE id = %s", (aid,))
        connection.commit()
        return get_answer_by_id(aid) == None

def delete_answer_by_question_id(qid: int):
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute("DELETE FROM answers WHERE question_id = %s", (qid,))
        connection.commit()
        return get_all_answers_by_question_id(qid) == None

