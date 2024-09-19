from api.data_api import get_data
from models.User import User
from repository.database import get_db_connection, create_users_table
from typing import List, Optional

from repository.user_answer_repository import delete_user_answer_by_user_id


def create_user(user: User) -> int:
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute("""
            INSERT INTO users (first, last, email)
            VALUES (%s, %s ,%s) RETURNING id
        """, (user.first, user.last, user.email))
        new_id = cursor.fetchone()['id']
        connection.commit()
        return new_id

def load_users_from_api():
    if get_all_users() is None or len(get_all_users()) < 5:
        users = get_data('https://randomuser.me/api?results=4')['results']
        for u in [User(first=u['name']['first'], last=u['name']['last'], email=u['email']) for u in users]:
            create_user(u)

def get_all_users() -> List[User]:
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute("SELECT * FROM users")
        res = cursor.fetchall()
        users = [User(**u) for u in res]
        return users if users else None


def get_user_by_id(uid: int) -> Optional[User]:
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute("SELECT * FROM users WHERE id = %s", (uid,))
        user = cursor.fetchone()
        return None if not user else User(**user)


def update_user(uid: int, user: User) -> User:
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute(
            "UPDATE users SET first = %s, last = %s, email = %s WHERE id = %s",
            (user.first, user.last, user.email, uid)
        )
        connection.commit()
        user = get_user_by_id(uid)
        return user

def delete_user(uid: int):
    if get_user_by_id(uid) == None:
        return False
    delete_user_answer_by_user_id(uid)
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute("DELETE FROM users WHERE id = %s", (uid,))
        connection.commit()
        return get_user_by_id(uid) == None

