import openai
import fitz
import nltk
import os
import re
from collections import Counter
from nltk.tokenize import word_tokenize
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# NLTK dependencies
nltk.download('punkt')
nltk.download('stopwords')

from nltk.corpus import stopwords

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Store questions
questions_store = []

#  API Key
openai.api_key = "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"


# Extract text from PDF
def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        with fitz.open(pdf_path) as doc:
            for page in doc:
                text += page.get_text()
        return text.strip()
    except Exception as e:
        return f"Not able to read PDF: {e}"


# Extract and validate
def extract_top_words(text, num_words=10):
    words = word_tokenize(text.lower())
    words = [word for word in words if word.isalpha()]
    words = [word for word in words if word not in stopwords.words("english")]
    freq_dist = Counter(words)
    return [word for word, _ in freq_dist.most_common(num_words)]


# Generate math question based on a word
def generate_math_question(word):
    prompt = f"Generate a simple math question based on the word '{word}'. It should be a basic arithmetic question with four answer choices, one of which is correct. Format: \n\nQuestion: <math question>\nA) <option 1>\nB) <option 2>\nC) <option 3>\nD) <option 4>\nCorrect Answer: <correct option letter>"

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )

    response_text = response['choices'][0]['message']['content'].strip()

    # Extract question, options, and answer
    lines = response_text.split("\n")
    question = lines[0].replace("Question: ", "").strip()
    options = [line.strip() for line in lines[1:5] if line.strip()]
    correct_answer = lines[-1].replace("Correct Answer: ", "").strip()

    return {
        "word": word,
        "question": question,
        "options": options,
        "correct_answer": correct_answer
    }


# Process PDF and generate
def process_pdf_and_generate_questions(pdf_path):
    global questions_store
    questions_store.clear()

    pdf_text = extract_text_from_pdf(pdf_path)
    if not pdf_text:
        return

    top_words = extract_top_words(pdf_text, 10)

    for word in top_words:
        question_data = generate_math_question(word)
        questions_store.append(question_data)


# Upload and process PDF
@app.route('/upload', methods=['POST'])
def upload_file():
    global questions_store
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    process_pdf_and_generate_questions(file_path)

    return jsonify({"message": "Questions generated successfully"})


# submit answers and normalized
@app.route('/submit_answers', methods=['POST'])
def submit_answers():
    data = request.json
    user_answers = data.get('answers', {})

    correct_count = 0
    incorrect_count = 0
    results = []

    for idx, question in enumerate(questions_store):
        correct_answer = question["correct_answer"].strip().lower()
        user_answer = user_answers.get(str(idx), "").strip().lower()

        result = "Correct" if user_answer == correct_answer else "Incorrect"

        if result == "Correct":
            correct_count += 1
        else:
            incorrect_count += 1

        results.append({
            "question": question["question"],
            "user_answer": user_answer,
            "correct_answer": correct_answer,
            "result": result
        })

    # Calculate  percentage
    total_answers = len(questions_store)
    correct_percentage = (correct_count / total_answers) * 100 if total_answers > 0 else 0

    #  level
    if correct_percentage > 75:
        level = "High Level"
    elif 45 <= correct_percentage <= 75:
        level = "Medium Level"
    else:
        level = "Low Level"

    # Save
    with open("math_results_summary.txt", "w") as file:
        file.write(f"{level}\n")
    with open("math_results_summary.txt", "r") as file:
        level_from_file = file.read().strip()

    return jsonify({
        "results": results,
        "correct_count": correct_count,
        "incorrect_count": incorrect_count,
        "correct_percentage": correct_percentage,
        "level": level_from_file
    })


# Get generated
@app.route('/get_questions', methods=['GET'])
def get_questions():
    return jsonify({"questions": questions_store})


# get levels
@app.route('/get_level', methods=['GET'])
def get_level():
    """Retrieve the level from the saved file."""
    try:
        with open("math_results_summary.txt", "r") as file:
            level = file.read().strip()
        return jsonify({"level": level})
    except Exception as e:
        return jsonify({"error": "Unable to read level from file"}), 500


if __name__ == '__main__':
    app.run(debug=True)
