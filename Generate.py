import random
from nltk.tokenize import sent_tokenize, word_tokenize
import nltk
nltk.download('punkt')


# Generate  question and answer
def generate_question_answer(paragraph, seed=42):
    # Set the random
    random.seed(seed)

    # Tokenize
    sentences = sent_tokenize(paragraph)
    questions = []

    while sentences:
        # select sentence
        sentence = random.choice(sentences)

        # Tokenize the selected sentence
        words = word_tokenize(sentence)
        pos_tags = nltk.pos_tag(words)
        entities = [word for word, pos in pos_tags if pos.startswith('NN') or pos.startswith('NNP')]

        if entities:
            entity = random.choice(entities)

            # Generate
            question = f"What is {entity} in the following sentence? " + sentence
            options = [sent for sent in sentences if sent != sentence and entity not in word_tokenize(sent)]
            random.shuffle(options)

            questions.append({"question": question, "options": options})


        sentences.remove(sentence)

    return questions
