# import random
# import spacy
# from utils import categorize_difficulty
# from sentence_transformers import SentenceTransformer, util
# from config import keywords
# nlp = spacy.load("en_core_web_sm")
#
# import random
#
#
# def generate_question_and_options(paragraph, keywords):
#     doc = nlp(paragraph)
#
#     # Identify important terms
#     nouns = [token.text for token in doc if token.pos_ in ['NOUN', 'PROPN']]
#     entities = [ent.text for ent in doc.ents]
#
#     # Determine difficulty level
#     difficulty = categorize_difficulty(paragraph, keywords)
#
#     # Identify which keyword matched the paragraph
#     matched_keyword = None
#     for level, words in keywords.items():
#         for word in words:
#             if word in paragraph.lower():
#                 matched_keyword = word
#                 break
#         if matched_keyword:
#             break  # Stop searching once we find a match
#
#     print(f"Difficulty Level: {difficulty} | Matched Keyword: {matched_keyword}")
#
#     # Generate questions based on difficulty
#     if difficulty == "Low Level":
#         question = f"What is {entities[0]}?" if entities else f"What is {nouns[0]}?" if nouns else "What is this about?"
#     elif difficulty == "Medium Level":
#         question = f"Why is {entities[0]} important?" if entities else f"Why is {nouns[0]} significant?"
#     elif difficulty == "High Level":
#         question = f"How does {entities[0]} impact {nouns[1]}?" if len(
#             entities) > 1 else f"Explain the role of {nouns[0]}."
#
#     # Generate answer choices
#     correct_answer = paragraph[:100] + "..." if len(paragraph) > 100 else paragraph
#     sentences = [sent.text for sent in doc.sents]
#
#     # Filter sentences to avoid irrelevant or off-topic answers
#     relevant_sentences = [sent for sent in sentences if len(sent.split()) > 3]  # Exclude very short sentences
#
#     incorrect_answers = random.sample(relevant_sentences, min(3, len(relevant_sentences))) if len(
#         relevant_sentences) > 1 else []
#
#     while len(incorrect_answers) < 3:
#         incorrect_answers.append("Random incorrect statement.")  # Fallback in case there aren't enough relevant answers
#
#     # Make sure options are shuffled and valid
#     options = [correct_answer] + incorrect_answers
#     random.shuffle(options)
#
#     # Filter out answers that may not make sense (e.g., irrelevant entities like "2" or "3" being treated as answers)
#     options = [opt for opt in options if not any(char.isdigit() for char in opt)]
#
#     return {
#         "question": question,
#         "options": options,
#         "correct_answer": correct_answer,
#         "difficulty": difficulty,
#         "matched_keyword": matched_keyword  # Returning the matched keyword for debugging
#     }
#
#
# def filter_important_paragraphs(paragraphs, difficulty):
#     """Filter important paragraphs based on difficulty level and matching keywords."""
#     important_paragraphs = []
#
#     for paragraph in paragraphs:
#         doc = nlp(paragraph)
#         entities = [ent.text.lower() for ent in doc.ents]  # Extract named entities
#
#         # Debugging print: Show extracted entities
#         print(f"\nParagraph: {paragraph[:100]}...")
#         print(f"Extracted entities: {entities}")
#
#         # Check keyword match based on difficulty
#         if difficulty == "High Level":
#             matched_keywords = [word for word in keywords['high_level'] if word in entities]
#         elif difficulty == "Medium Level":
#             matched_keywords = [word for word in keywords['medium_level'] if word in entities]
#         elif difficulty == "Low Level":
#             matched_keywords = [word for word in keywords['low_level'] if word in entities]
#         else:
#             matched_keywords = []
#
#         # Debugging print: Show matched keywords
#         print(f"Matched keywords for {difficulty}: {matched_keywords}")
#
#         if matched_keywords:
#             important_paragraphs.append(paragraph)
#
#     # If no paragraphs matched, return all paragraphs to avoid empty output
#     if not important_paragraphs:
#         print(f"No important paragraphs found for {difficulty}. Using all available paragraphs.")
#         return paragraphs
#
#     return important_paragraphs
#
#
# def rule_based_filter(question):
#     if len(question.split()) < 10:  # Too short to be meaningful
#         return False
#     if "?" not in question:  # If it doesn't end with a question mark
#         return False
#     return True
#
# # BERT model initialization
# model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
#
# def bert_similarity(paragraph, question):
#     # Get embeddings for both paragraph and question
#     paragraph_embedding = model.encode(paragraph)
#     question_embedding = model.encode(question)
#
#     # Compute cosine similarity between the embeddings
#     similarity = util.pytorch_cos_sim(paragraph_embedding, question_embedding)
#
#     return similarity.item()  # Similarity score between 0 and 1

import random
import spacy
from utils import categorize_difficulty
from sentence_transformers import SentenceTransformer, util
from config import keywords
import json

nlp = spacy.load("en_core_web_sm")

# BERT model initialization
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

def save_questions_to_file(question_data, filename="generated_questions.json"):


    try:
        with open(filename, "r") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []

    # Check if the question already exists
    existing_questions = {item["question"] for item in data}

    if question_data["question"] not in existing_questions:
        data.append(question_data)

        with open(filename, "w") as file:
            json.dump(data, file, indent=4)
        print("Question saved successfully.")
    else:
        print("Duplicate question detected. Skipping save.")


def generate_software_engineering_question(paragraph, keywords):
    """Generate software engineering specific questions based on paragraph content"""
    doc = nlp(paragraph)

    # Extract technology terms and concepts
    tech_terms = extract_tech_terms(doc)
    software_concepts = extract_software_concepts(doc)

    # Determine difficulty level
    difficulty = categorize_difficulty(paragraph, keywords)

    # Find matched keyword for debugging
    matched_keyword = find_matched_keyword(paragraph, keywords)
    print(f"Difficulty Level: {difficulty} | Matched Keyword: {matched_keyword}")

    # Generate question based on difficulty and content
    if not tech_terms and not software_concepts:
        # Fallback for paragraphs without clear tech terms
        question = generate_generic_question(doc, difficulty)
    else:
        question = generate_tech_specific_question(tech_terms, software_concepts, difficulty)

    # Generate answer choices
    answer_choices = generate_answer_choices(doc, paragraph, tech_terms, software_concepts)

    # Ensure the correct answer is included and is concise
    correct_answer = select_correct_answer(doc, tech_terms, software_concepts)

    # Make sure correct answer is in the options
    if correct_answer not in answer_choices:
        answer_choices[-1] = correct_answer

    # Shuffle options
    random.shuffle(answer_choices)

    question_data = {
        "question": question,
        "options": answer_choices,
        "correct_answer": correct_answer,
        "difficulty": difficulty,
        "matched_keyword": matched_keyword
    }

    save_questions_to_file(question_data)
    return question_data


def extract_tech_terms(doc):
    """Extract technology terms from the document"""
    # Common software engineering technologies and frameworks
    tech_patterns = [
        "flask", "django", "python", "java", "javascript", "react", "angular", "vue",
        "node.js", "sql", "mysql", "mongodb", "postgresql", "nosql", "api", "rest",
        "graphql", "docker", "kubernetes", "aws", "azure", "google cloud", "serverless",
        "microservices", "devops", "ci/cd", "git", "github", "bitbucket", "jenkins",
        "figma", "bootstrap", "tailwind", "css", "html", "xml", "json", "yaml",
        "machine learning", "artificial intelligence", "nlp", "neural network",
        "deep learning", "data science", "big data", "hadoop", "spark", "tableau",
        "power bi", "sqlalchemy", "orm", "mvc", "mvvm", "oauth", "jwt", "api key",
        "agile", "scrum", "kanban", "waterfall", "sprint", "backlog"
    ]

    found_terms = []
    for term in tech_patterns:
        if term in doc.text.lower():
            found_terms.append(term)

    # Also include named entities that might be tech-related
    for ent in doc.ents:
        if ent.label_ in ["ORG", "PRODUCT"] or ent.text.lower() in tech_patterns:
            found_terms.append(ent.text)

    return list(set(found_terms))  # Remove duplicates


def extract_software_concepts(doc):
    """Extract software engineering concepts from the document"""
    concept_patterns = [
        "architecture", "design pattern", "module", "component", "interface",
        "api", "database", "schema", "model", "view", "controller", "frontend",
        "backend", "full-stack", "scalability", "performance", "security",
        "authentication", "authorization", "encryption", "hashing", "testing",
        "unit test", "integration test", "e2e test", "deployment", "monitoring",
        "logging", "debugging", "maintenance", "refactoring", "code quality",
        "technical debt", "documentation", "versioning", "api gateway", "load balancing",
        "caching", "indexing", "query optimization", "normalization", "denormalization",
        "data modeling", "object-oriented", "functional programming", "reactive programming",
        "event-driven", "concurrency", "threading", "asynchronous", "synchronous",
        "distributed system", "fault tolerance", "high availability", "disaster recovery",
        "rollback", "deployment", "continuous integration", "continuous delivery",
        "rbac", "access control", "user experience", "user interface", "responsive design",
        "mobile-first", "accessibility", "internationalization", "localization"
    ]

    found_concepts = []
    doc_lower = doc.text.lower()

    for concept in concept_patterns:
        if concept in doc_lower:
            found_concepts.append(concept)

    return list(set(found_concepts))  # Remove duplicates


def find_matched_keyword(paragraph, keywords):
    """Find which keyword matched the paragraph"""
    paragraph_lower = paragraph.lower()

    for level, words in keywords.items():
        for word in words:
            if word in paragraph_lower:
                return word

    return None


def generate_generic_question(doc, difficulty):
    """Generate a generic question when no specific tech terms or concepts are found"""
    sentences = [sent.text for sent in doc.sents]

    if difficulty == "Low Level":
        return "Which of the following is true about software development?"
    elif difficulty == "Medium Level":
        return "What is the main advantage described in the following software engineering concept?"
    else:  # High Level
        return "Which of the following best describes the advanced software engineering principle discussed?"


def generate_tech_specific_question(tech_terms, software_concepts, difficulty):
    """Generate technology-specific questions based on difficulty level"""
    if not tech_terms and not software_concepts:
        return "What is the main software engineering concept discussed in the text?"

    # Choose a random tech term or concept to focus on
    focus_terms = tech_terms if tech_terms else software_concepts
    primary_term = random.choice(focus_terms)

    if difficulty == "Low Level":
        question_templates = [
            f"What is {primary_term} used for in software development?",
            f"Which of the following best describes {primary_term}?",
            f"How is {primary_term} implemented in software systems?",
            f"What is the primary purpose of {primary_term} in software engineering?"
        ]
    elif difficulty == "Medium Level":
        question_templates = [
            f"How does {primary_term} contribute to software system architecture?",
            f"What advantage does {primary_term} provide in software engineering?",
            f"How does {primary_term} integrate with other components in a software system?",
            f"What role does {primary_term} play in modern software development?"
        ]
    else:  # High Level
        if len(focus_terms) > 1:
            secondary_term = random.choice([t for t in focus_terms if t != primary_term])
            question_templates = [
                f"How does {primary_term} enhance {secondary_term} in software architecture?",
                f"What is the relationship between {primary_term} and {secondary_term} in complex software systems?",
                f"When implementing {primary_term}, how does it affect the overall {secondary_term} strategy?",
                f"How would you optimize a system that uses both {primary_term} and {secondary_term}?"
            ]
        else:
            question_templates = [
                f"What are the advanced implementation considerations for {primary_term}?",
                f"How does {primary_term} affect scalability and performance in enterprise systems?",
                f"What are the security implications of implementing {primary_term}?",
                f"How would you evaluate the effectiveness of {primary_term} in a distributed system?"
            ]

    return random.choice(question_templates)


def generate_answer_choices(doc, paragraph, tech_terms, software_concepts):
    """Generate plausible answer choices for the question"""
    sentences = [sent.text for sent in doc.sents]

    # Filter sentences to contain relevant information
    relevant_sentences = []
    for sent in sentences:
        if len(sent.split()) > 5 and len(sent.split()) < 30:  # Reasonable length
            has_relevance = False
            for term in tech_terms + software_concepts:
                if term.lower() in sent.lower():
                    has_relevance = True
                    break
            if has_relevance:
                relevant_sentences.append(sent)

    # If we don't have enough relevant sentences, use other sentences
    if len(relevant_sentences) < 3:
        relevant_sentences.extend([s for s in sentences if len(s.split()) > 5 and len(s.split()) < 30])

    # Ensure we have at least 4 options
    if len(relevant_sentences) >= 4:
        return random.sample(relevant_sentences, 4)
    else:
        # Generate some generic answers if we don't have enough sentences
        generic_answers = [
            "It provides a scalable architecture for enterprise applications.",
            "It improves system performance through optimized algorithms.",
            "It enhances security by implementing encryption and access controls.",
            "It simplifies development through modular components and abstractions.",
            "It reduces technical debt by enforcing coding standards and best practices.",
            "It enables cross-platform compatibility through standardized interfaces.",
            "It streamlines the development process through automated workflows."
        ]

        result = relevant_sentences.copy()
        while len(result) < 4:
            random_answer = random.choice(generic_answers)
            if random_answer not in result:
                result.append(random_answer)

        return result


def select_correct_answer(doc, tech_terms, software_concepts):
    """Select the best sentence as the correct answer"""
    sentences = [sent.text for sent in doc.sents]

    best_sentence = None
    best_score = -1

    for sent in sentences:
        # Skip very short or very long sentences
        if len(sent.split()) < 5 or len(sent.split()) > 30:
            continue

        # Count how many tech terms and concepts are in the sentence
        score = 0
        for term in tech_terms + software_concepts:
            if term.lower() in sent.lower():
                score += 1

        if score > best_score:
            best_score = score
            best_sentence = sent

    # If no good sentence found, use the first sentence that's not too short
    if not best_sentence:
        for sent in sentences:
            if len(sent.split()) >= 5:
                best_sentence = sent
                break

    # If still no good sentence, create a generic answer
    if not best_sentence:
        if tech_terms:
            best_sentence = f"{tech_terms[0]} is a key technology used in modern software development."
        elif software_concepts:
            best_sentence = f"{software_concepts[0]} is an important concept in software engineering."
        else:
            best_sentence = "Software engineering involves designing and implementing scalable, maintainable systems."

    return best_sentence


def filter_important_paragraphs(paragraphs, difficulty):
    """Filter important paragraphs based on difficulty level and matching keywords."""
    important_paragraphs = []

    # First, extract tech terms from all paragraphs to get a comprehensive list
    all_tech_terms = set()
    all_software_concepts = set()

    for paragraph in paragraphs:
        doc = nlp(paragraph)
        tech_terms = extract_tech_terms(doc)
        software_concepts = extract_software_concepts(doc)
        all_tech_terms.update(tech_terms)
        all_software_concepts.update(software_concepts)

    # Print for debugging
    print(f"All extracted tech terms: {list(all_tech_terms)}")
    print(f"All extracted software concepts: {list(all_software_concepts)}")

    # Now filter paragraphs based on difficulty and relevance
    for paragraph in paragraphs:
        doc = nlp(paragraph)

        # Extract tech terms and concepts for this paragraph
        tech_terms = extract_tech_terms(doc)
        software_concepts = extract_software_concepts(doc)

        # Debugging print
        print(f"\nParagraph: {paragraph[:100]}...")
        print(f"Extracted tech terms: {tech_terms}")
        print(f"Extracted software concepts: {software_concepts}")

        # Check keyword match based on difficulty
        matched_keywords = []

        if difficulty == "High Level":
            # High level: paragraphs with multiple advanced concepts
            if len(tech_terms) >= 2 and len(software_concepts) >= 2:
                matched_keywords = ["advanced_software_engineering"]
        elif difficulty == "Medium Level":
            # Medium level: paragraphs with specific frameworks or tools
            for term in tech_terms:
                if term.lower() in ["flask", "django", "react", "angular", "docker", "kubernetes",
                                    "machine learning", "sqlalchemy", "bootstrap"]:
                    matched_keywords.append(term.lower())
        elif difficulty == "Low Level":
            # Low level: paragraphs with basic concepts
            basic_concepts = ["database", "interface", "frontend", "backend", "testing", "documentation"]
            for concept in software_concepts:
                if concept.lower() in basic_concepts:
                    matched_keywords.append(concept.lower())

        # Debugging print
        print(f"Matched keywords for {difficulty}: {matched_keywords}")

        if matched_keywords:
            important_paragraphs.append(paragraph)

    # If no paragraphs matched, return all paragraphs to avoid empty output
    if not important_paragraphs:
        print(f"No important paragraphs found for {difficulty}. Using all available paragraphs.")
        return paragraphs

    return important_paragraphs


def rule_based_filter(question):
    """Filter questions based on quality rules"""
    if len(question.split()) < 7:  # Too short to be meaningful
        return False
    if "?" not in question:  # If it doesn't end with a question mark
        return False
    # Avoid questions that are too generic
    if question in ["What is this about?", "Explain the role of."]:
        return False
    return True


def bert_similarity(paragraph, question):
    """Calculate similarity between paragraph and question using BERT embeddings"""
    # Get embeddings for both paragraph and question
    paragraph_embedding = model.encode(paragraph)
    question_embedding = model.encode(question)

    # Compute cosine similarity between the embeddings
    similarity = util.pytorch_cos_sim(paragraph_embedding, question_embedding)

    return similarity.item()  # Similarity score between 0 and 1


def process_paragraphs_for_questions(paragraphs, difficulty_level):
    """Process paragraphs and generate questions based on difficulty level"""
    important_paragraphs = filter_important_paragraphs(paragraphs, difficulty_level)
    print(f"Found {len(important_paragraphs)} important paragraphs for difficulty level: {difficulty_level}")

    questions = []
    for paragraph in important_paragraphs:
        print(f"\nChecking difficulty for paragraph: {paragraph[:100]}...")
        question_data = generate_software_engineering_question(paragraph, keywords)

        # Only include question if it passes quality filters
        if rule_based_filter(question_data["question"]):
            questions.append(question_data)
            print(f"Generated question: {question_data}")

    return questions