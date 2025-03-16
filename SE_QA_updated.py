import fitz
from transformers import AutoTokenizer, AutoModelForQuestionAnswering, pipeline
from sentence_transformers import SentenceTransformer, util
import random
import json
import logging

# Setup logging
logging.basicConfig(filename='qa_generation.log', level=logging.INFO)

# Models
bert_model_name = "bert-large-uncased-whole-word-masking-finetuned-squad"
tokenizer = AutoTokenizer.from_pretrained(bert_model_name)
qa_model = AutoModelForQuestionAnswering.from_pretrained(bert_model_name)
qa_pipeline = pipeline("question-answering", model=qa_model, tokenizer=tokenizer)

sentence_model = SentenceTransformer("all-MiniLM-L6-v2")



# Generate questions and answers
def generate_question_answer_bert(paragraph, seed=42):
    random.seed(seed)

    # Handle long paragraphs
    if len(paragraph.split()) > 512:
        paragraph = " ".join(paragraph.split()[:512])

    try:
        # Generate a question
        question = f"What is the main idea of the following passage? {paragraph}"
        answer = qa_pipeline({'context': paragraph, 'question': question})['answer']

        # Split sentences for distractors
        sentences = [sent.strip() for sent in paragraph.split(". ") if sent and answer not in sent]

        # Generate distractors using semantic similarity
        distractors = generate_distractors(answer, sentences)

        # Combine correct and incorrect options
        options = distractors + [answer]
        random.shuffle(options)

        return [{"question": question, "options": options}]
    except Exception as e:
        logging.error(f"Error generating QA: {e}")
        return []

# Generate distractors
def generate_distractors(answer, sentences):
    distractors = []
    try:
        answer_embedding = sentence_model.encode(answer, convert_to_tensor=True)
        sentence_embeddings = sentence_model.encode(sentences, convert_to_tensor=True)
        similarity_scores = util.pytorch_cos_sim(answer_embedding, sentence_embeddings).squeeze()

        # Select top distinct sentences
        sorted_indices = similarity_scores.argsort(descending=True)
        for idx in sorted_indices[:3]:  # Top 3 distractors
            distractors.append(sentences[idx])
    except Exception as e:
        logging.error(f"Error generating distractors: {e}")
    return distractors

# Convert PDF to text
def convert_pdf_to_text(pdf_path):
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()
    return text

# Format question data
def format_question_data(question_data):
    formatted_output = json.dumps(question_data, indent=4)
    return formatted_output

def clean_text(text):
    text = text.replace("\n", " ")  # Replace newlines with spaces
    text = text.replace("\u2022", "-")  # Replace Unicode bullets with a dash
    text = text.replace("o  ", "")  # Handle stray 'o' if it's unintended
    return text.strip()  # Remove leading and trailing whitespace

# File paths
pdf_paths = ["Notes1.pdf", "Notes2.pdf"]
question_data = []

# Process PDFs
for pdf_path in pdf_paths:
    print(f"Processing PDF: {pdf_path}")
    logging.info(f"Processing PDF: {pdf_path}")

    pdf_text = convert_pdf_to_text(pdf_path)

    # Split text into paragraphs
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
        paragraph = clean_text(paragraph)
        questions = generate_question_answer_bert(paragraph)
        if questions:
            question_data.append(
                {"pdf_path": pdf_path, "question": questions[0]["question"], "options": questions[0]["options"]}
            )

formatted_data = format_question_data(question_data)
print(formatted_data)
# Save to JSON file
output_file = "qa_data.json"
formatted_data = format_question_data(question_data)
with open(output_file, "w", encoding="utf-8") as file:
    file.write(formatted_data)

print(f"QA data saved to {output_file}")
