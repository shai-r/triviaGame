from dataclasses import asdict
from flask import Blueprint, jsonify, request
from dto.ResponseDto import ResponseDto
from models.Answer import Answer
from models.Question import Question
from repository.answer_repository import get_all_answers, create_answer, get_answer_by_id, update_answer, \
    get_all_answers_by_question_id, delete_answer, delete_answer_by_question_id
from repository.question_repository import get_all_questions, create_question, get_question_by_id, update_question, \
    delete_question
from repository.user_answer_repository import get_all_user_answers, create_user_answer, \
    get_all_user_answers_by_question_id
from repository.user_repository import *

questions_blueprint = Blueprint("questions", __name__)

@questions_blueprint.route("/", methods=['GET'])
def all_questions():
    return jsonify(asdict(ResponseDto(body=get_all_questions()))), 200

@questions_blueprint.route("/create", methods=['POST'])
def add_question():
    question = Question(**request.json)
    uid = create_question(question)
    question.id = uid
    return jsonify(asdict(ResponseDto(body=question))), 201

@questions_blueprint.route("/<int:question_id>", methods=['GET'])
def question_by_id(question_id):
    question = get_question_by_id(question_id)
    return ((jsonify(asdict(ResponseDto(body=question))), 200) if question else
            (jsonify(asdict(ResponseDto(error='not found'))), 404))

@questions_blueprint.route("/update/<int:question_id>", methods=['PUT'])
def set_question(question_id):
    question = update_question(question_id, Question(**request.json))
    return ((jsonify(asdict(ResponseDto(body=question))), 201) if question else
            (jsonify(asdict(ResponseDto(error='not found'))), 404))

@questions_blueprint.route("/delete/<int:question_id>", methods=['DELETE'])
def remove_question(question_id):
    is_deleted = delete_question(question_id)
    return jsonify(asdict(ResponseDto(message=is_deleted))), 200 if is_deleted else 404


@questions_blueprint.route("/answers", methods=['GET'])
def all_answers():
    return jsonify(asdict(ResponseDto(body=get_all_answers()))), 200

@questions_blueprint.route("/answers/question=<int:question_id>", methods=['GET'])
def all_answers_by_question(question_id):
    return jsonify(asdict(ResponseDto(body=get_all_answers_by_question_id(question_id)))), 200

@questions_blueprint.route("/answers/create", methods=['POST'])
def add_answer():
    answer = Answer(**request.json)
    uid = create_answer(answer)
    answer.id = uid
    return jsonify(asdict(ResponseDto(body=answer))), 201

@questions_blueprint.route("/answers/<int:answer_id>", methods=['GET'])
def answer_by_id(answer_id):
    answer = get_answer_by_id(answer_id)
    return ((jsonify(asdict(ResponseDto(body=answer))), 200) if answer else
            (jsonify(asdict(ResponseDto(error='not found'))), 404))

@questions_blueprint.route("/answers/update/<int:answer_id>", methods=['PUT'])
def set_answer(answer_id):
    answer = update_answer(answer_id, Answer(**request.json))
    return ((jsonify(asdict(ResponseDto(body=answer))), 201) if answer else
            (jsonify(asdict(ResponseDto(error='not found'))), 404))

@questions_blueprint.route("/answers/delete/<int:answer_id>", methods=['DELETE'])
def remove_answer(answer_id):
    is_deleted = delete_answer(answer_id)
    return jsonify(asdict(ResponseDto(message=is_deleted))), 200 if is_deleted else 404

@questions_blueprint.route("/answers/delete/question=<int:question_id>", methods=['DELETE'])
def remove_answer_by_question(question_id):
    is_deleted = delete_answer_by_question_id(question_id)
    return jsonify(asdict(ResponseDto(message=is_deleted))), 200 if is_deleted else 404