import fitz
import Generate as QA


def convert_pdf_to_text(pdf_path):
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()
    return text


def adjust_options(options, correct_answer):
    valid_options = [opt for opt in options if opt.strip().lower() != "none of the above"]

    if not valid_options:
        return ["Error in option generation", "Check question logic", "None of the above", "None of the above"], "None of the above"

    while len(valid_options) < 3:
        valid_options.append("None of the above")

    if correct_answer not in valid_options:
        valid_options.append(correct_answer)
    
    return valid_options[:4], correct_answer


def validate_options(options):
    return options.count("None of the above") <= 1


def format_question_data(question_data):
    formatted_output = ""

    for item in question_data:
        formatted_output += f"Question: {item['question']}\n"
        formatted_output += "Options:\n"
        for idx, option in enumerate(item['options'], 1):
            formatted_output += f"  {idx}. {option}\n"
        formatted_output += f"Correct Answer: {item['answer']}\n\n"

    return formatted_output


pdf_paths = ["Notes1.pdf"]
question_data = []

for pdf_path in pdf_paths:
    print("Processing:", pdf_path)
    pdf_text = convert_pdf_to_text(pdf_path)
    doc = fitz.open(pdf_path)
    extracted_paragraphs = []
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        page_text = page.get_text("text")
        paragraphs = page_text.split("\n \n")
        extracted_paragraphs.extend([p.strip() for p in paragraphs if p.strip()])
    
    doc.close()

    for paragraph in extracted_paragraphs:
        questions = QA.generate_question_answer(paragraph)

        if questions:
            for q in questions:
                if not q["options"]:
                    continue

                correct_answer = q.get("answer", "None of the above")
                formatted_options, correct_answer = adjust_options(q["options"], correct_answer)
                
                if not validate_options(formatted_options):
                    continue
                
                question_data.append(
                    {"question": q["question"], "options": formatted_options, "answer": correct_answer}
                )

formatted_data = format_question_data(question_data)
print(formatted_data)

