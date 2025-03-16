import fitz
from transformers import AutoTokenizer, AutoModelForQuestionAnswering, pipeline
import random

# BERT
model_name = "bert-large-uncased-whole-word-masking-finetuned-squad"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForQuestionAnswering.from_pretrained(model_name)
qa_pipeline = pipeline("question-answering", model=model, tokenizer=tokenizer)


# Generate questions  and  answers
def generate_question_answer_bert(paragraph, seed=42):
    random.seed(seed)


    if len(paragraph.split()) > 512:
        paragraph = " ".join(paragraph.split()[:512])

    try:
        # question
        question = f"What is the main idea of the following passage? {paragraph}"

        # pipeline
        answer = qa_pipeline({'context': paragraph, 'question': question})['answer']

        # Tokenize
        sentences = paragraph.split(". ")
        sentences = [sent.strip() for sent in sentences if sent and answer not in sent]


        incorrect_options = random.sample(sentences, min(len(sentences), 3))

        # Combine correct and incorrect options
        options = incorrect_options + [answer]
        random.shuffle(options)

        return [{"question": question, "options": options}]
    except Exception as e:
        print(f"Error generating QA: {e}")
        return []


# Convert a PDF to text
def convert_pdf_to_text(pdf_path):
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()
    return text


# structured manner
def format_question_data(question_data):
    formatted_output = ""
    for item in question_data:
        formatted_output += f"PDF: {item['pdf_path']}\n"
        formatted_output += f"Question: {item['question']}\nOptions:\n"
        for idx, option in enumerate(item['options'], 1):
            formatted_output += f"  {idx}. {option}\n"
        formatted_output += "\n"
    return formatted_output


# file paths
pdf_paths = ["Notes1.pdf","Notes2.pdf"]
question_data = []

# Loop
for pdf_path in pdf_paths:
    print(f"Processing PDF: {pdf_path}")


    pdf_text = convert_pdf_to_text(pdf_path)

    # Split the text into paragraphs
    doc = fitz.open(pdf_path)
    extracted_paragraphs = []
    for page_num in range(len(doc)):
        page = doc[page_num]
        page_text = page.get_text()
        paragraphs = page_text.split("\n \n")
        extracted_paragraphs.extend(paragraphs)
    doc.close()

    # Generate questions from each paragraph
    for paragraph in extracted_paragraphs:
        questions = generate_question_answer_bert(paragraph)
        if questions:
            question_data.append(
                {"pdf_path": pdf_path, "question": questions[0]["question"], "options": questions[0]["options"]})


formatted_data = format_question_data(question_data)
print(formatted_data)
