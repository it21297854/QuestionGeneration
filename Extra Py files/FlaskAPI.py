from flask import Flask, request, jsonify
import fitz
import os
import Generate as QA
app = Flask(__name__)
from datetime import datetime
import json

def convert_pdf_to_text(pdf_path):
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()
    return text



def format_question_data(question_data):
    formatted_output = ""

    for item in question_data:
        if "message" in item:
            formatted_output += f"PDF: {item['pdf_path']}\nMessage: {item['message']}\n\n"
        else:
            formatted_output += f"Question: {item['question']}\n"
            formatted_output += "Options:\n"
            for idx, option in enumerate(item['options'], 1):
                formatted_output += f"  {idx}. {option}\n"
            formatted_output += "\n"

    return formatted_output


@app.route('/upload_pdf', methods=['POST'])
def upload_pdf():
    if 'pdf_file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    pdf_file = request.files['pdf_file']
    if pdf_file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if pdf_file and pdf_file.filename.endswith('.pdf'):
        file_path = os.path.join("../uploads", pdf_file.filename)
        pdf_file.save(file_path)
        return jsonify({'message': 'PDF file uploaded successfully', 'file_path': file_path}), 200
    else:
        return jsonify({'error': 'Invalid file type'}), 400


@app.route('/process_pdf', methods=['POST'])
def process_pdf():
    data = request.get_json()
    if not data or 'pdf_paths' not in data:
        return jsonify({'error': 'PDF paths are required'}), 400

    pdf_paths = data['pdf_paths']
    question_data = []

    for pdf_path in pdf_paths:
        try:
            print("Processing:", pdf_path)
            pdf_text = convert_pdf_to_text(pdf_path)


            doc = fitz.open(pdf_path)
            extracted_paragraphs = []
            for page_num in range(len(doc)):
                page = doc[page_num]
                page_text = page.get_text()
                paragraphs = page_text.split("\n \n")
                extracted_paragraphs.extend(paragraphs)
            doc.close()

            # Generate questions
            for paragraph in extracted_paragraphs:
                questions = QA.generate_question_answer(paragraph)

                if questions:
                    # Append
                    question_data.append(
                        {"pdf_path": pdf_path, "question": questions[0]["question"], "options": questions[0]["options"]}
                    )
                else:
                    question_data.append(
                        {"pdf_path": pdf_path, "message": "No questions generated for this paragraph."})

        except Exception as e:
            return jsonify({'error': f"Error processing {pdf_path}: {str(e)}"}), 500


    formatted_data = format_question_data(question_data)
    return jsonify({'formatted_data': formatted_data}), 200

@app.route('/process_pdf_structured', methods=['POST'])
def process_pdf_structured():
    data = request.get_json()
    if not data or 'pdf_paths' not in data:
        return jsonify({'error': 'PDF paths are required'}), 400

    pdf_paths = data['pdf_paths']
    question_data = []

    for pdf_path in pdf_paths:
        try:
            print("Processing:", pdf_path)
            pdf_text = convert_pdf_to_text(pdf_path)

            # Open PDF and extract paragraphs
            doc = fitz.open(pdf_path)
            extracted_paragraphs = []
            for page_num in range(len(doc)):
                page = doc[page_num]
                page_text = page.get_text()
                paragraphs = page_text.split("\n \n")
                extracted_paragraphs.extend(paragraphs)
            doc.close()

            # Generate questions
            pdf_questions = []
            for paragraph in extracted_paragraphs:
                questions = QA.generate_question_answer(paragraph)

                if questions:
                    for question in questions:
                        pdf_questions.append({
                            "question": question["question"],
                            "options": question["options"]
                        })
                else:
                    pdf_questions.append({
                        "message": "No questions generated for this paragraph."
                    })

            # Append structured data
            question_data.append({
                "pdf_path": pdf_path,
                "questions": pdf_questions
            })

        except Exception as e:
            return jsonify({'error': f"Error processing {pdf_path}: {str(e)}"}), 500

    # Beautify output
    beautified_data = []
    for pdf_entry in question_data:
        pdf_path = pdf_entry["pdf_path"]
        beautified_data.append(f"PDF File: {pdf_path}\n")

        for question in pdf_entry["questions"]:
            if "question" in question:
                beautified_data.append("Question:")
                beautified_data.append(f"  {question['question']}")
                beautified_data.append("Options:")
                for idx, option in enumerate(question["options"], start=1):
                    beautified_data.append(f"  {idx}. {option}")
                beautified_data.append("")  # Add an empty line for readability
            else:
                beautified_data.append("Message:")
                beautified_data.append(f"  {question['message']}")
                beautified_data.append("")  # Add an empty line for readability

    # Combine beautified data
    beautified_output = "\n".join(beautified_data)

    return jsonify({'beautified_data': beautified_output}), 200

# File to store user engagement data
ENGAGEMENT_FILE = "user_engagement.txt"

# Sample questions based on engagement levels
QUESTIONS = {
    "low": "What motivates you to engage more with the platform?",
    "medium": "What features do you find most useful?",
    "high": "Would you recommend this platform to others?"
}

# Function to log engagement data
def log_engagement_data(user_id, activity_type, metadata=None):
    engagement_data = {
        "user_id": user_id,
        "activity_type": activity_type,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "metadata": metadata
    }
    try:
        with open(ENGAGEMENT_FILE, "a") as file:
            file.write(json.dumps(engagement_data) + "\n")
        return True
    except Exception as e:
        print(f"Error logging engagement: {e}")
        return False

# Function to calculate engagement level
def calculate_engagement_level(percentage):
    if percentage < 40:
        return "low"
    elif 40 <= percentage < 70:
        return "medium"
    else:
        return "high"

# Function to fetch question based on engagement level
def get_question_for_user(percentage):
    engagement_level = calculate_engagement_level(percentage)
    return QUESTIONS.get(engagement_level, "No question available.")

# Function to read engagement logs
def read_engagement_logs():
    try:
        with open(ENGAGEMENT_FILE, "r") as file:
            logs = file.readlines()
            engagement_logs = [json.loads(log.strip()) for log in logs]
            return engagement_logs
    except FileNotFoundError:
        return []

# API Endpoints
@app.route('/log-engagement', methods=['POST'])
def log_engagement():
    """Log user engagement."""
    data = request.json
    user_id = data.get('user_id')
    activity_type = data.get('activity_type')
    metadata = data.get('metadata')

    if not user_id or not activity_type:
        return jsonify({"error": "user_id and activity_type are required"}), 400

    success = log_engagement_data(user_id, activity_type, metadata)
    if success:
        return jsonify({"message": "Engagement logged successfully"}), 200
    else:
        return jsonify({"error": "Failed to log engagement"}), 500

@app.route('/get-question', methods=['GET'])
def get_question():
    """Get a question for the user based on engagement percentage."""
    percentage = request.args.get('percentage', type=float)
    if percentage is None:
        return jsonify({"error": "percentage is required"}), 400

    question = get_question_for_user(percentage)
    return jsonify({"engagement_level": calculate_engagement_level(percentage), "question": question})

# @app.route('/engagement-logs', methods=['GET'])
# def engagement_logs():
#     """Fetch all engagement logs."""
#     logs = read_engagement_logs()
#     return jsonify({"logs": logs})


@app.route('/engagement-logs', methods=['GET'])
def get_engagement_logs():
    user_id = request.args.get('user_id', type=int)

    # Read all logs
    logs = read_engagement_logs()

    # If user_id is provided, filter the logs for the specific user
    if user_id is not None:
        logs = [log for log in logs if log.get('user_id') == user_id]

    return jsonify({'logs': logs}), 200

@app.route('/calculate-level', methods=['GET'])
def calculate_level():
    """Calculate engagement level for a given percentage."""
    percentage = request.args.get('percentage', type=float)
    if percentage is None:
        return jsonify({"error": "percentage is required"}), 400

    engagement_level = calculate_engagement_level(percentage)
    return jsonify({"engagement_level": engagement_level})

if __name__ == '__main__':

    if not os.path.exists('../uploads'):
        os.makedirs('../uploads')

    app.run(debug=True)
