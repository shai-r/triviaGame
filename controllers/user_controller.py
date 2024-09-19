from dataclasses import asdict
from datetime import timedelta

from flask import Blueprint, jsonify, request
from dto.ResponseDto import ResponseDto
from models.UserAnswer import UserAnswer
from repository.user_answer_repository import get_all_user_answers, create_user_answer, get_user_answer_by_id, \
    update_user_answer, delete_user_answer
from repository.user_repository import *

user_blueprint = Blueprint("user", __name__)

@user_blueprint.route("/", methods=['GET'])
def all_users():
    return jsonify(asdict(ResponseDto(body=get_all_users()))), 200

@user_blueprint.route("/create", methods=['POST'])
def add_user():
    user = User(**request.json)
    uid = create_user(user)
    user.id = uid
    return jsonify(asdict(ResponseDto(body=user))), 201

@user_blueprint.route("/<int:user_id>", methods=['GET'])
def user_by_id(user_id):
    user = get_user_by_id(user_id)
    return ((jsonify(asdict(ResponseDto(body=user))), 200) if user else
            (jsonify(asdict(ResponseDto(error='not found'))), 404))

@user_blueprint.route("/update/<int:user_id>", methods=['PUT'])
def update(user_id):
    user = update_user(user_id, User(**request.json))
    return ((jsonify(asdict(ResponseDto(body=user))), 201) if user else
            (jsonify(asdict(ResponseDto(error='not found'))), 404))

@user_blueprint.route("/delete/<int:user_id>", methods=['DELETE'])
def delete(user_id):
    is_deleted = delete_user(user_id)
    return jsonify(asdict(ResponseDto(message=is_deleted))), 200 if is_deleted else 404

@user_blueprint.route("/answer/", methods=['GET'])
def all_user_answers():
    # create_user_answer(
    #     UserAnswer(
    #         user_id=1,
    #         question_id=1,
    #         answer_text="yes!!!",
    #         is_correct=True,
    #         time_taken=timedelta(milliseconds=10000)
    #     )
    # )
    # create_user_answer(
    #     UserAnswer(
    #         user_id=2,
    #         question_id=1,
    #         answer_text="yews!!!",
    #         is_correct=True,
    #         time_taken=timedelta(milliseconds=100000)
    #     )
    # )
    return jsonify(asdict(ResponseDto(body=get_all_user_answers()))), 200

@user_blueprint.route("/answer/create", methods=['POST'])
def add_user_answers():
    user_answers = UserAnswer(**request.json)
    uid = create_user_answer(user_answers)
    user_answers.id = uid
    return jsonify(asdict(ResponseDto(body=user_answers))), 201

@user_blueprint.route("/answer/<int:user_answer_id>", methods=['GET'])
def user_answer_by_id(user_answer_id):
    user_answer = get_user_answer_by_id(user_answer_id)
    return ((jsonify(asdict(ResponseDto(body=user_answer))), 200) if user_answer else
            (jsonify(asdict(ResponseDto(error='not found'))), 404))

@user_blueprint.route("/answer/update/<int:user_answer_id>", methods=['PUT'])
def put_user_answer(user_answer_id):
    user_answer = update_user_answer(user_answer_id, UserAnswer(**request.json))
    return ((jsonify(asdict(ResponseDto(body=user_answer))), 201) if user_answer else
            (jsonify(asdict(ResponseDto(error='not found'))), 404))

@user_blueprint.route("/answer/delete/<int:user_answer_id>", methods=['DELETE'])
def remove_user_answer(user_answer_id):
    is_deleted = delete_user_answer(user_answer_id)
    return jsonify(asdict(ResponseDto(message=is_deleted))), 200 if is_deleted else 404