import pytest
from repository.database import create_all_tables, drop_all_tables
from repository.user_repository import *
from models.User import User

@pytest.fixture(scope="module")
def setup_database():
    create_all_tables()
    load_users_from_api()
    yield
    drop_all_tables()

def test_create_user(setup_database):
    new_id = create_user(User(first='Shai',last='Reiner',email='y9651951'))
    assert new_id == 5

def test_get_all_users(setup_database):
    users = get_all_users()
    assert users

def test_get_user_by_id(setup_database):
    user = get_user_by_id(3)
    assert user.id == 3

def test_update_user(setup_database):
    update_user(3, User(first='Shai',last='Reiner',email='y9651951'))
    user = get_user_by_id(3)
    assert user.first =='Shai'

def test_delete_user(setup_database):
    assert delete_user(3)
