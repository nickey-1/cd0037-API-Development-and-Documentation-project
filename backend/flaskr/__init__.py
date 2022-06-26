import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from sqlalchemy import type_coerce

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

# Utility method for pagination


def paginate_elements(elements):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE  # starting index
    end = start + QUESTIONS_PER_PAGE  # ending index

    formatted_elements = [element.format() for element in elements]
    current_elements = formatted_elements[start:end]

    return current_elements


def create_app(test_config=None):
    # Create and configure the app
    app = Flask(__name__)
    setup_db(app)

    # Enable cors
    cors = CORS(app, resources={"/api/*": {"origins": "*"}})

    # Set cors headers
    @app.after_request
    def after_request(response):
        """
        Method sets access control
        """

        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,POST,PATCH,DELETE,OPTIONS')

        return response

    @app.route('/api/categories')
    def get_categories():
        """
        Method is responsible for getting all categories
        :return:
        """

        # Get all categories and add to a dictionary
        categories = Category.query.all()

        categories_dict = {}

        for category in categories:
            categories_dict[category.id] = category.type

        # 404 error if no category was found
        if len(categories_dict) == 0:
            abort(404)

        # Return json data to view
        return jsonify({
            'categories': categories_dict,
            'success': True
        })

    @app.route('/api/questions')
    def get_questions():
        """
         Method is responible for getting all questions
        :return:
        """

        # Get all questions ordered by difficulty and paginate
        questions = Question.query.order_by(Question.difficulty).all()
        current_questions = paginate_elements(questions)

        # Get all categories and add to a dictionary
        categories = Category.query.all()
        categories_dict = {}

        for category in categories:
            categories_dict[category.id] = category.type

        # 404 if no question was found
        if len(current_questions) == 0:
            abort(404)

        # Return json data to view
        return jsonify({
            'categories': categories_dict,
            'questions': current_questions,
            'current_category': [],
            'success': True,
            'questions_per_page': len(current_questions),
            'total_questions': len(Question.query.all())
        })

    @app.route('/api/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        """
        Method is responsible for deleting a specific question by ID
        :param question_id:
        :return:
        """
        try:
            # Get question by id
            question = Question.query.filter_by(id=question_id).one_or_none()

            # 404 if no question was found(if None)
            if question is None:
                abort(404)

            # Delete the question
            question.delete()

            # Get the paginated list of questions
            questions = Question.query.order_by(Question.difficulty).all()
            current_questions = paginate_elements(questions)

            # Return json data to view and show id deleted
            return jsonify({
                'questions': current_questions,
                'deleted': question_id,
                'success': True,
                'questions_per_page': len(current_questions),
                'total_questions': len(Question.query.all())
            })
        except:
            # 422 if problem arises deleting a specific question
            abort(422)

    @app.route('/api/questions', methods=['POST'])
    def post_question():
        """
        Method is responsible for posting and searching for a question
        :return:
        """

        # Load and parse the request body
        body = request.get_json()

        # Is search term present?
        if body.get('searchTerm'):
            search_term = body.get('searchTerm')

            # Get the search term from the request
            search_term = request.json.get('searchTerm')

            # Query using search_term
            search_result = Question.query.filter(
                Question.question.ilike(f'%{search_term}%')).all()

            # 404 if no result is found
            if len(search_result) == 0:
                abort(404)

            # Paginate search result
            current_search_result = paginate_elements(search_result)

            # return json data to view
            return jsonify({
                'success': True,
                'questions': current_search_result,
                'total_questions': len(current_search_result)
            })
        else:
            # Load data from the request body
            question = body.get('question', '')
            answer = body.get('answer', '')
            category = body.get('category', '')
            difficulty = body.get('difficulty', '')

            # 422 if all data fields are not populated
            if (question == '') or (answer == '') or (category == '') or (difficulty == ''):
                abort(422)

            try:
                question = Question(
                    question=question, answer=answer, category=category, difficulty=difficulty)

                # Create a new question
                question.insert()

                # Get the paginated list of questions
                questions = Question.query.order_by(Question.difficulty).all()

                current_questions = paginate_elements(questions)

                # Return json data to view and show id created
                return jsonify({
                    'questions': current_questions,
                    'question_created': question.question,
                    'created': question.id,
                    'success': True,
                    'questions_per_page': len(current_questions),
                    'total_questions': len(Question.query.all())
                })
            except:
                # 422 if problem arises creating a new question
                abort(422)

    @app.route('/api/categories/<int:category_id>/questions')
    def get_questions_by_category(category_id):
        """
        Method is responsible for getting questions based on a particular category.
        :param category_id:
        :return:
        """
        
        # Get the category by id
        category = Category.query.filter_by(id=category_id).one_or_none()

        # abort if no category was found
        if category is None:
            abort(400)

        current_category = category.type

        questions_by_category = Question.query.filter_by(
            category=str(category.id)).all()
        current_questions_by_category = paginate_elements(
            questions_by_category)

        # Return json data to view
        return jsonify({
            'current_category': current_category,
            'questions': current_questions_by_category,
            'success': True,
            'questions_per_page': len(current_questions_by_category),
            'total_questions': len(Question.query.all())
        })

    @app.route('/api/quizzes', methods=['POST'])
    def get_random_quiz_question():
        """
        Method is responsible for the functionality of playing a quiz
        :return:
        """

        try:
            # Load the request body
            body = request.get_json()

            # 400 if required parameters are not supplied
            if not ('quiz_category' in body and 'previous_questions' in body):
                abort(400)

            # Load data from the request body
            category = body.get('quiz_category')
            previous_questions = body.get('previous_questions')

            # Load available questions of a particular category
            if category['type'] == 'click':
                available_questions = Question.query.filter(
                    Question.id.notin_(previous_questions)).all()
            else:
                available_questions = Question.query.filter_by(
                    category=category['id']).filter(Question.id.notin_(previous_questions)).all()

            # Generate a new random question
            new_question = available_questions[random.randrange(
                0, len(available_questions))].format() if len(available_questions) > 0 else None

            # Return json data to view
            return jsonify({
                'success': True,
                'question': new_question
            })
        except:
            abort(400)

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    # Expected error handlers

    @app.errorhandler(400)
    def bad_request(error):

        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(404)
    def not_found(error):

        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):

        return jsonify({
            "success": False,
            "error": 405,
            "message": "method not allowed"
        }), 405

    @app.errorhandler(422)
    def unprocessable(error):

        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(500)
    def server_error(error):

        return jsonify({
            'success': False,
            'error': 500,
            "message": "server error"
        })

    return app
