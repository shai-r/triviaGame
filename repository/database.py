import psycopg2
from psycopg2.extras import RealDictCursor
from config.sql_config import SQL_URI

def get_db_connection():
    return psycopg2.connect(SQL_URI, cursor_factory=RealDictCursor)

def create_users_table():
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            first VARCHAR(255) NOT NULL,
            last VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL
            )
        ''')
    connection.commit()

def create_questions_table():
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS questions (
            id SERIAL PRIMARY KEY,
            question_text VARCHAR(255) NOT NULL,
            correct_answer VARCHAR(255) NOT NULL
            )
        ''')
    connection.commit()

def create_answers_table():
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS answers (
                id SERIAL PRIMARY KEY,
                question_id INTEGER NOT NULL,
                incorrect_answer VARCHAR(255) NOT NULL,
                FOREIGN KEY (question_id) 
                    REFERENCES questions(id) 
                        ON DELETE CASCADE
            )
        ''')
    connection.commit()

def create_user_answers_table():
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_answers (
                id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL,
                question_id INTEGER NOT NULL,
                answer_text VARCHAR(255) NOT NULL,
                is_correct BOOLEAN NOT NULL,
                time_taken VARCHAR(255) NOT NULL,
                FOREIGN KEY (user_id) 
                    REFERENCES users(id) 
                        ON DELETE CASCADE,
                FOREIGN KEY (question_id) 
                    REFERENCES questions(id) 
                        ON DELETE CASCADE
            )
        ''')
    connection.commit()

def create_all_tables():
    create_users_table()
    create_questions_table()
    create_answers_table()
    create_user_answers_table()

def drop_users_table():
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute("DROP TABLE IF EXISTS users")
        connection.commit()

def drop_questions_table():
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute("DROP TABLE IF EXISTS questions")
        connection.commit()


def drop_answers_table():
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute("DROP TABLE IF EXISTS answers")
        connection.commit()

def drop_user_answers_table():
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute("DROP TABLE IF EXISTS user_answers")
        connection.commit()

def drop_all_tables():
    drop_user_answers_table()
    drop_answers_table()
    drop_questions_table()
    drop_users_table()