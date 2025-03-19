import random
import spacy
from utils import categorize_difficulty
from sentence_transformers import SentenceTransformer, util
from config import keywords
nlp = spacy.load("en_core_web_sm")

import random


def generate_question_and_options(paragraph, keywords):
    doc = nlp(paragraph)

    # Identify important terms
    nouns = [token.text for token in doc if token.pos_ in ['NOUN', 'PROPN']]
    entities = [ent.text for ent in doc.ents]

    # Determine difficulty level
    difficulty = categorize_difficulty(paragraph, keywords)

    # Identify which keyword matched the paragraph
    matched_keyword = None
    for level, words in keywords.items():
        for word in words:
            if word in paragraph.lower():
                matched_keyword = word
                break
        if matched_keyword:
            break  # Stop searching once we find a match

    print(f"Difficulty Level: {difficulty} | Matched Keyword: {matched_keyword}")

    # Generate questions based on difficulty
    if difficulty == "Low Level":
        question = f"What is {entities[0]}?" if entities else f"What is {nouns[0]}?" if nouns else "What is this about?"
    elif difficulty == "Medium Level":
        question = f"Why is {entities[0]} important?" if entities else f"Why is {nouns[0]} significant?"
    elif difficulty == "High Level":
        question = f"How does {entities[0]} impact {nouns[1]}?" if len(
            entities) > 1 else f"Explain the role of {nouns[0]}."

    # Generate answer choices
    correct_answer = paragraph[:100] + "..." if len(paragraph) > 100 else paragraph
    sentences = [sent.text for sent in doc.sents]

    # Filter sentences to avoid irrelevant or off-topic answers
    relevant_sentences = [sent for sent in sentences if len(sent.split()) > 3]  # Exclude very short sentences

    incorrect_answers = random.sample(relevant_sentences, min(3, len(relevant_sentences))) if len(
        relevant_sentences) > 1 else []

    while len(incorrect_answers) < 3:
        incorrect_answers.append("Random incorrect statement.")  # Fallback in case there aren't enough relevant answers

    # Make sure options are shuffled and valid
    options = [correct_answer] + incorrect_answers
    random.shuffle(options)

    # Filter out answers that may not make sense (e.g., irrelevant entities like "2" or "3" being treated as answers)
    options = [opt for opt in options if not any(char.isdigit() for char in opt)]

    return {
        "question": question,
        "options": options,
        "correct_answer": correct_answer,
        "difficulty": difficulty,
        "matched_keyword": matched_keyword  # Returning the matched keyword for debugging
    }


def filter_important_paragraphs(paragraphs, difficulty):
    """Filter important paragraphs based on difficulty level and matching keywords."""
    important_paragraphs = []

    for paragraph in paragraphs:
        doc = nlp(paragraph)
        entities = [ent.text.lower() for ent in doc.ents]  # Extract named entities

        # Debugging print: Show extracted entities
        print(f"\nParagraph: {paragraph[:100]}...")
        print(f"Extracted entities: {entities}")

        # Check keyword match based on difficulty
        if difficulty == "High Level":
            matched_keywords = [word for word in keywords['high_level'] if word in entities]
        elif difficulty == "Medium Level":
            matched_keywords = [word for word in keywords['medium_level'] if word in entities]
        elif difficulty == "Low Level":
            matched_keywords = [word for word in keywords['low_level'] if word in entities]
        else:
            matched_keywords = []

        # Debugging print: Show matched keywords
        print(f"Matched keywords for {difficulty}: {matched_keywords}")

        if matched_keywords:
            important_paragraphs.append(paragraph)

    # If no paragraphs matched, return all paragraphs to avoid empty output
    if not important_paragraphs:
        print(f"No important paragraphs found for {difficulty}. Using all available paragraphs.")
        return paragraphs

    return important_paragraphs


def rule_based_filter(question):
    if len(question.split()) < 10:  # Too short to be meaningful
        return False
    if "?" not in question:  # If it doesn't end with a question mark
        return False
    return True

# BERT model initialization
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

def bert_similarity(paragraph, question):
    # Get embeddings for both paragraph and question
    paragraph_embedding = model.encode(paragraph)
    question_embedding = model.encode(question)

    # Compute cosine similarity between the embeddings
    similarity = util.pytorch_cos_sim(paragraph_embedding, question_embedding)

    return similarity.item()  # Similarity score between 0 and 1
