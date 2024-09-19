from models.UserAnswer import UserAnswer
from repository.database import get_db_connection
from typing import List, Optional

def create_user_answer(user_answer: UserAnswer) -> int:
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute("""
            INSERT INTO user_answers (user_id, question_id, answer_text, is_correct, time_taken)
            VALUES (%s ,%s, %s, %s, %s) RETURNING id
        """, (user_answer.user_id,
              user_answer.question_id,
              user_answer.answer_text,
              user_answer.is_correct,
              user_answer.time_taken))
        new_id = cursor.fetchone()['id']
        connection.commit()
        return new_id

def get_all_user_answers() -> List[UserAnswer]:
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute("SELECT * FROM user_answers")
        res = cursor.fetchall()
        user_answer = [UserAnswer(**ua) for ua in res]
        return user_answer if len(user_answer) > 0 else None


def get_user_answer_by_id(uaid: int) -> Optional[UserAnswer]:
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute("SELECT * FROM user_answers WHERE id = %s", (uaid,))
        user_answer = cursor.fetchone()
        return None if not user_answer else UserAnswer(**user_answer)

def get_all_user_answers_by_user_id(uid: int) -> Optional[UserAnswer]:
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute("SELECT * FROM user_answers WHERE user_id = %s", (uid,))
        res = cursor.fetchall()
        user_answer = [UserAnswer(**ua) for ua in res]
        return user_answer if len(user_answer) > 0 else None

def get_all_user_answers_by_question_id(qid: int) -> Optional[UserAnswer]:
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute("SELECT * FROM user_answers WHERE question_id = %s", (qid,))
        res = cursor.fetchall()
        user_answer = [UserAnswer(**ua) for ua in res]
        return user_answer if len(user_answer) > 0 else None

def get_all_user_answers_by_correct_answer(correct: bool) -> Optional[UserAnswer]:
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute("SELECT * FROM user_answers WHERE is_correct = %s", (correct,))
        res = cursor.fetchall()
        user_answer = [UserAnswer(**ua) for ua in res]
        return user_answer if len(user_answer) > 0 else None

def update_user_answer(uaid: int, user_answer: UserAnswer) -> UserAnswer:
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute(
            "UPDATE user_answers SET "
            "user_id = %s, "
            "question_id = %s, "
            "answer_text = %s, "
            "is_correct = %s, "
            "time_taken = %s "
            "WHERE id = %s",
            (user_answer.user_id,
             user_answer.question_id,
             user_answer.answer_text,
             user_answer.is_correct,
             user_answer.time_taken,
             uaid)
        )
        connection.commit()
        user_answer = get_user_answer_by_id(uaid)
        return user_answer

def delete_user_answer(uaid: int):
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute("DELETE FROM user_answers WHERE id = %s", (uaid,))
        connection.commit()
        return get_user_answer_by_id(uaid) == None

def delete_user_answer_by_user_id(uid: int):
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute("DELETE FROM user_answers WHERE user_id = %s", (uid,))
        connection.commit()
        return get_all_user_answers_by_user_id(uid) == None

def delete_user_answer_by_question_id(qid: int):
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute("DELETE FROM user_answers WHERE question_id = %s", (qid,))
        connection.commit()
        return get_all_user_answers_by_question_id(qid) == None
