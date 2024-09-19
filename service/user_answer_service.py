# from models.UserAnswer import UserAnswer
# from repository.user_answer_repository import get_all_user_answers, create_user_answer
#
#
# def seed_user_answers():
#     if get_all_user_answers() is None or len(get_all_user_answers()) < 10:
#         create_user_answer(UserAnswer(user_id=1,question_id=1,))
#
#         user_id: int
#         question_id: int
#         answer_text: str
#         is_correct: bool
#         time_taken: timedelta