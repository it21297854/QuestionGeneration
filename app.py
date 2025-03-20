from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from file_handler import extract_paragraphs_from_pdf, extract_paragraphs_from_word, extract_paragraphs_from_ppt,clean_text
from nlp_processor import generate_software_engineering_question, categorize_difficulty, filter_important_paragraphs
from utils import read_level_from_file, save_level_to_file

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Store questions
questions_store = []

# Expanded IT-related keywords for each level
keywords = {
    'high_level': [
        'machine_learning', 'natural_language_processing', 'optical_character_recognition',
        'deep_learning', 'cybersecurity', 'artificial_intelligence', 'quantum_computing',
        'blockchain', 'predictive_models', 'threat_detection', 'neural_networks', 'cloud_security',
        'edge_computing', 'autonomous_systems', 'big_data', 'data_science', 'computer_vision',
        'reinforcement_learning', 'internet_of_things', '5G_technology'
    ],
    'medium_level': [
        'flask', 'mysql', 'sqlalchemy', 'bootstrap', 'figma', 'role_based_access_control',
        'data_management', 'database_schema', 'security_testing', 'performance_optimization',
        'horizontal_scaling', 'devops', 'docker', 'cloud_computing', 'encryption',
        'referential_integrity', 'modular_architecture', 'api_integration', 'microservices',
        'containerization', 'serverless_architecture', 'continuous_integration'
    ],
    'low_level': [
        'modular_design', 'user_interface', 'responsive_design', 'mobile_compatibility',
        'authentication', 'authorization', 'secure_authentication', 'system_performance',
        'UI_UX_principles', 'data_consistency', 'software_architecture', 'scalability',
        'secure_access_control', 'index_numbers', 'real_time_feedback', 'dynamic_UI',
        'session_management', 'load_balancing', 'cross_browser_compatibility', 'web_accessibility',
        'error_handling', 'form_validation', 'data_validation', 'debugging'
    ]
}


@app.route('/upload', methods=['POST'])
def upload_file():
    global questions_store
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file part"}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400

        # Reset the questions_store for new file
        questions_store = []

        # Save the uploaded file
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)

        file_ext = file.filename.split('.')[-1].lower()
        if file_ext == 'pdf':
            paragraphs = extract_paragraphs_from_pdf(file_path)
        elif file_ext == 'docx':
            paragraphs = extract_paragraphs_from_word(file_path)
        elif file_ext == 'txt':
            with open(file_path, 'r') as f:
                paragraphs = [line.strip() for line in f.readlines() if line.strip()]
        elif file_ext in ['ppt', 'pptx']:
            paragraphs = extract_paragraphs_from_ppt(file_path)
        else:
            return jsonify({"error": "Unsupported file type"}), 400

        # Debugging step: print number of paragraphs extracted
        print(f"Number of paragraphs extracted: {len(paragraphs)}")

        cleaned_paragraphs = [clean_text(p) for p in paragraphs]
        print(f"Cleaned {len(cleaned_paragraphs)} paragraphs")

        difficulty_level = read_level_from_file()
        print(f"Difficulty level read from file: {difficulty_level}")

        # Filter important paragraphs based on the difficulty level
        important_paragraphs = filter_important_paragraphs(cleaned_paragraphs, difficulty_level)
        print(f"Found {len(important_paragraphs)} important paragraphs for difficulty level: {difficulty_level}")

        # Generate questions for important paragraphs
        generated_questions = []
        for p in important_paragraphs[:5]:  # Limit to top 5 important paragraphs
            question_data = generate_software_engineering_question(p, keywords)
            print(f"Generated question: {question_data}")  # Debugging line
            if question_data:  # Check if the question is valid
                generated_questions.append(question_data)

        # Debugging step: print number of generated questions
        print(f"Generated {len(generated_questions)} questions")

        # Store the generated questions
        questions_store = generated_questions

        if not questions_store:
            return jsonify({"error": "No questions generated from the file."}), 500

        return jsonify({"message": "Questions generated successfully", "questions_count": len(generated_questions)})

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

@app.route('/get_questions', methods=['GET'])
def get_questions():
    level_from_file = read_level_from_file()
    return jsonify({"questions": questions_store, "level": level_from_file})

@app.route('/submit_answers', methods=['POST'])
def submit_answers():
    """Evaluate answers and return results."""
    data = request.json
    user_answers = data.get('answers', {})

    correct_count = 0
    incorrect_count = 0
    results = []

    # Iterate
    for idx, question in enumerate(questions_store):
        correct_answer = question["correct_answer"]
        user_answer = user_answers.get(str(idx), "")
        result = "Correct" if user_answer == correct_answer else "Incorrect"

        # Count correct and incorrect answers
        if result == "Correct":
            correct_count += 1
        else:
            incorrect_count += 1

        results.append({
            "question": question["question"],
            "user_answer": user_answer,
            "correct_answer": correct_answer,
            "result": result,
            "difficulty": question["difficulty"]
        })

    # Calculate percentage
    total_answers = len(questions_store)
    correct_percentage = (correct_count / total_answers) * 100 if total_answers > 0 else 0

    # Determine level based on percentage
    if correct_percentage > 75:
        level = "High Level"
    elif 45 <= correct_percentage <= 75:
        level = "Medium Level"
    else:
        level = "Low Level"

    save_level_to_file(level)

    level_from_file = read_level_from_file()

    return jsonify({
        "results": results,
        "correct_count": correct_count,
        "incorrect_count": incorrect_count,
        "correct_percentage": correct_percentage,
        "level": level_from_file
    })

@app.route('/get_level', methods=['GET'])
def get_level():
    try:
        level = read_level_from_file()
        return jsonify({"level": level})
    except Exception as e:
        return jsonify({"error": "Unable to read level from file"}), 500

import json


@app.route('/get_questions_by_difficulty', methods=['GET'])
def get_questions_by_difficulty():
    difficulty = request.args.get(
        'difficulty')  # Get the difficulty parameter from the query string (low, medium, high)

    # Check for valid difficulty values based on the saved data format
    valid_difficulties = ['Low Level', 'Medium Level', 'High Level']
    if difficulty not in valid_difficulties:
        return jsonify(
            {"error": "Invalid difficulty. Please choose from 'Low Level', 'Medium Level', or 'High Level'."}), 400

    # Read the saved questions from the JSON file
    try:
        with open('generated_questions.json', 'r') as f:
            questions_data = json.load(f)

        # Filter questions based on the difficulty
        questions_for_difficulty = [q for q in questions_data if q['difficulty'] == difficulty]

        if not questions_for_difficulty:
            return jsonify({"message": f"No questions found for difficulty: {difficulty}."}), 404

        return jsonify({"questions": questions_for_difficulty}), 200

    except Exception as e:
        return jsonify({"error": f"Error reading questions: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(debug=True)

# import os
# import traceback
# from flask import Flask, request, jsonify
# from werkzeug.utils import secure_filename
# from nlp_processor import (
#     process_paragraphs_for_questions,
#     filter_important_paragraphs,
#     generate_software_engineering_question
# )
# from file_handler import (
#     extract_paragraphs_from_pdf,
#     extract_paragraphs_from_word,
#     extract_paragraphs_from_ppt
# )
# from file_handler import clean_text
# from config import keywords, default_config, file_config
#
# app = Flask(__name__)
#
# # Configure upload folder
# UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config['MAX_CONTENT_LENGTH'] = file_config['max_file_size_mb'] * 1024 * 1024  # MB to bytes
#
# # Global store for generated questions
# questions_store = []
#
#
# def read_level_from_file():
#     """Read the selected difficulty level from file"""
#     try:
#         with open('level.txt', 'r') as f:
#             return f.read().strip()
#     except FileNotFoundError:
#         # Return default level if file doesn't exist
#         return default_config['default_difficulty']
#
#
# @app.route('/get_level', methods=['GET'])
# def get_level():
#     difficulty_level = read_level_from_file()
#     return jsonify({"level": difficulty_level})
#
#
# @app.route('/set_level', methods=['POST'])
# def set_level():
#     data = request.get_json()
#     if 'level' not in data:
#         return jsonify({"error": "No level provided"}), 400
#
#     level = data['level']
#     if level not in ["Low Level", "Medium Level", "High Level"]:
#         return jsonify({"error": "Invalid level"}), 400
#
#     # Write the level to file
#     with open('level.txt', 'w') as f:
#         f.write(level)
#
#     return jsonify({"message": f"Level set to {level}"})
#
#
# @app.route('/upload', methods=['POST'])
# def upload_file():
#     global questions_store
#     try:
#         if 'file' not in request.files:
#             return jsonify({"error": "No file part"}), 400
#
#         file = request.files['file']
#         if file.filename == '':
#             return jsonify({"error": "No selected file"}), 400
#
#         # Reset the questions_store for new file
#         questions_store = []
#
#         # Check file extension
#         file_ext = file.filename.split('.')[-1].lower()
#         if file_ext not in file_config['allowed_extensions']:
#             return jsonify(
#                 {"error": f"Unsupported file type. Allowed types: {', '.join(file_config['allowed_extensions'])}"}), 400
#
#         # Save the uploaded file securely
#         filename = secure_filename(file.filename)
#         file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#         file.save(file_path)
#
#         # Extract paragraphs based on file type
#         paragraphs = []
#         if file_ext == 'pdf':
#             paragraphs = extract_paragraphs_from_pdf(file_path)
#         elif file_ext == 'docx':
#             paragraphs = extract_paragraphs_from_word(file_path)
#         elif file_ext == 'txt':
#             with open(file_path, 'r', encoding='utf-8') as f:
#                 # Split by double newlines to get paragraphs
#                 content = f.read()
#                 paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
#         elif file_ext in ['ppt', 'pptx']:
#             paragraphs = extract_paragraphs_from_ppt(file_path)
#
#         # Debugging: print number of paragraphs extracted
#         print(f"Number of paragraphs extracted: {len(paragraphs)}")
#
#         # Clean and filter the paragraphs
#         cleaned_paragraphs = []
#         for p in paragraphs:
#             cleaned = clean_text(p)
#             # Only include paragraphs with meaningful content
#             if len(cleaned.split()) >= default_config['min_paragraph_length'] / 5:  # Roughly words
#                 cleaned_paragraphs.append(cleaned)
#
#         print(f"Cleaned {len(cleaned_paragraphs)} paragraphs")
#
#         # Read the user's difficulty level from the file
#         difficulty_level = read_level_from_file()
#         print(f"Difficulty level read from file: {difficulty_level}")
#
#         # Process paragraphs and generate questions based on difficulty level
#         questions_store = process_paragraphs_for_questions(cleaned_paragraphs, difficulty_level)
#
#         # Limit to a reasonable number of questions if needed
#         max_questions = default_config['questions_per_request']
#         if len(questions_store) > max_questions:
#             questions_store = questions_store[:max_questions]
#
#         # Debugging: print number of generated questions
#         print(f"Generated {len(questions_store)} questions")
#
#         if not questions_store:
#             return jsonify({
#                 "warning": "No high-quality questions could be generated from this content. Try a different file or difficulty level.",
#                 "questions_count": 0
#             })
#
#         return jsonify({
#             "message": "Questions generated successfully",
#             "questions_count": len(questions_store)
#         })
#
#     except Exception as e:
#         # Print detailed error for debugging
#         print(f"Error in upload_file: {str(e)}")
#         print(traceback.format_exc())
#         return jsonify({"error": f"An error occurred: {str(e)}"}), 500
#
#
# @app.route('/get_questions', methods=['GET'])
# def get_questions():
#     global questions_store
#     if not questions_store:
#         return jsonify({"error": "No questions available. Please upload a file first."}), 404
#     return jsonify({"questions": questions_store})
#
#
# @app.route('/')
# def index():
#     return "AI Question Generator API is running. Use /upload to generate questions and /get_questions to retrieve them."
#
#
# if __name__ == '__main__':
#     app.run(debug=True)