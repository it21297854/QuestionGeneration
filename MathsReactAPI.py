import openai
import fitz
from nltk.tokenize import sent_tokenize
import nltk
import os
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# NLTK
nltk.download('punkt')

# LLM key
api_key = "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"
openai.api_key = api_key

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Store 
questions_store = []

# Extract
def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        with fitz.open(pdf_path) as doc:
            for page in doc:
                text += page.get_text()
        return text.strip()
    except Exception as e:
        return f"Not able to read PDF: {e}"

# Preprocess 
def preprocess_text_for_chunks(text, chunk_size=5):
    sentences = sent_tokenize(text)
    return [" ".join(sentences[i:i+chunk_size]) for i in range(0, len(sentences), chunk_size)]



def validate_questions(questions_text):
    questions = questions_text.strip().split("\n\n")
    for question in questions:
        lines = question.split("\n")
        if len(lines) < 6:
            return False, "Invalid"
        if not any(line.startswith("Correct Answer:") for line in lines):
            return False, "correct answer specified."
    return True, "valid."


# Generate math questions
def generate_math_questions(text_chunk):
    with open("results_summary.txt", "r") as file:
        level = file.read().strip()

    prompt = (
        f"Generate a mathematical question involving calculations such as addition, subtraction, multiplication, division, "
        f"or set operations at the level of '{level}'. The question must include four answer options. "
        f"Ensure the question is meaningful, and reject any questions that do not have exactly four options. "
        f"Base the question on the following text:\n{text_chunk}\n\nMathematical Question:")

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    response_text = response['choices'][0]['message']['content'].strip()
    
    # Parse  question, options, and correct answer
    lines = response_text.split("\n")
    question = lines[0].replace("Question: ", "")
    options = [line.strip() for line in lines[1:5] if line.strip()]
    correct_answer = lines[-1].replace("Correct Answer: ", "").strip()
    
    return {
        "question": question,
        "options": options,
        "correct_answer": correct_answer
    }

# Process PDF
def process_pdf_and_generate_questions(pdf_path):
    print(f"Processing: {pdf_path}")

    pdf_text = extract_text_from_pdf(pdf_path)
    if not pdf_text:
        print("No text.")
        return

    text_chunks = preprocess_text_for_chunks(pdf_text)

    for i, chunk in enumerate(text_chunks):
        print(f"\nProcessing Chunk {i+1}/{len(text_chunks)}...")
        result = generate_math_questions(chunk)
        print(f"\nGenerated Questions for Chunk {i+1}:")
        print(result)
        questions_store.append(result)

# Upload 
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

# Get questions 
@app.route('/get_questions', methods=['GET'])
def get_questions():
    return jsonify({"questions": questions_store})

# Submit answers 
@app.route('/submit_answers', methods=['POST'])
def submit_answers():
    data = request.json
    user_answers = data.get('answers', {})

    correct_count = 0
    incorrect_count = 0
    results = []

    # Iterate through 
    for idx, question in enumerate(questions_store):
        correct_answer = question["correct_answer"]
        user_answer = user_answers.get(str(idx), "")
        result = "Correct" if user_answer == correct_answer else "Incorrect"

        # Count answers
        if result == "Correct":
            correct_count += 1
        else:
            incorrect_count += 1

        results.append({
            "question": question["question"],
            "user_answer": user_answer,
            "correct_answer": correct_answer,
            "result": result,
            "difficulty": question.get("difficulty", "Unknown")  
        })

    #  percentage
    total_answers = len(questions_store)
    correct_percentage = (correct_count / total_answers) * 100 if total_answers > 0 else 0

    # level
    if correct_percentage > 75:
        level = "High Level"
    elif 45 <= correct_percentage <= 75:
        level = "Medium Level"
    else:
        level = "Low Level"

    # Save results and get
    with open("results_summary.txt", "w") as file:
        file.write(f"{level}\n")
    with open("results_summary.txt", "r") as file:
        level_from_file = file.read().strip()

    return jsonify({
        "results": results,
        "correct_count": correct_count,
        "incorrect_count": incorrect_count,
        "correct_percentage": correct_percentage,
        "level": level_from_file
    })


@app.route('/get_level', methods=['GET'])
def get_level():
    """Retrieve the level from the saved file."""
    try:
        with open("results_summary.txt", "r") as file:
            level = file.read().strip()
        return jsonify({"level": level})
    except Exception as e:
        return jsonify({"error": "Unable to read level from file"}), 500

if __name__ == '__main__':
    app.run(port=5001,debug=True)
