from flask import Flask, render_template, request
import fitz
import Generate as QA

app = Flask(__name__)

#  PDF to text
def convert_pdf_to_text(pdf_path):
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()
    return text


def adjust_options(options, correct_answer):
    valid_options = [opt for opt in options if opt.strip().lower() != "none of the above"]

    if not valid_options:
        return ["Error in option generation", "Check question logic", "None of the above", "None of the above"]

    while len(valid_options) < 3:
        valid_options.append("None of the above")

    valid_options.append(correct_answer)
    return valid_options[:4]

# Validation
def validate_options(options):
    none_of_the_above_count = 0
    for option in options:
        cleaned_option = option.strip().lower()
        if cleaned_option == "none of the above":
            none_of_the_above_count += 1

    if none_of_the_above_count > 1:
        return False

    return True

# Format structured manner
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

@app.route("/", methods=["GET", "POST"])
def display_questions():
    pdf_paths = ["Notes1.pdf"]
    question_data = []

    # Loop through each PDF
    for pdf_path in pdf_paths:
        print("Processing:", pdf_path)
        pdf_text = convert_pdf_to_text(pdf_path)

        # Extract paragraphs
        doc = fitz.open(pdf_path)
        extracted_paragraphs = []
        for page_num in range(len(doc)):
            page = doc[page_num]
            page_text = page.get_text("text")
            paragraphs = page_text.split("\n \n")
            extracted_paragraphs.extend([p.strip() for p in paragraphs if p.strip()])  # Remove empty paragraphs
        doc.close()

        # Generate questions
        for paragraph in extracted_paragraphs:
            questions = QA.generate_question_answer(paragraph)

            if questions:
                for q in questions:
                    if not q["options"]:  # Skip invalid questions
                        continue

                    correct_answer = q.get("answer", "No correct answer provided")
                    formatted_options = adjust_options(q["options"], correct_answer)

                    # Validate options to ensure no more than one "None of the above"
                    if not validate_options(formatted_options):
                        continue  # Skip this question if it has more than one "None of the above"

                    question_data.append(
                        {"pdf_path": pdf_path, "question": q["question"], "options": formatted_options, "correct_answer": correct_answer}
                    )

    if request.method == "POST":
        user_answers = request.form
        results = []

        for idx, question in enumerate(question_data):
            user_answer = user_answers.get(f"question_{idx}")
            correct_answer = question["correct_answer"]
            result = "Correct" if user_answer == correct_answer else "Incorrect"
            results.append({
                "question": question["question"],
                "user_answer": user_answer,
                "correct_answer": correct_answer,
                "result": result
            })

        return render_template("results.html", results=results)

    # Render the questions on GET request
    return render_template("questions.html", questions=question_data, enumerate=enumerate)

if __name__ == "__main__":
    app.run(debug=True)
