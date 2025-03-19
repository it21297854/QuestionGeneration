from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def categorize_difficulty(paragraph, keywords):
    """Categorize difficulty based on keyword presence and paragraph length."""
    print(f"\nChecking difficulty for paragraph: {paragraph[:100]}...")
    length = len(paragraph)

    # Check for high-level keywords first
    high_level_keywords = sum([paragraph.lower().count(keyword) for keyword in keywords['high_level']])
    medium_level_keywords = sum([paragraph.lower().count(keyword) for keyword in keywords['medium_level']])
    low_level_keywords = sum([paragraph.lower().count(keyword) for keyword in keywords['low_level']])

    # Assign difficulty based on keyword frequency and paragraph length
    if high_level_keywords > 2 or length > 500:  # Arbitrary threshold for high difficulty
        return 'High Level'
    elif medium_level_keywords > 2:
        return 'Medium Level'
    elif low_level_keywords > 2:
        return 'Low Level'
    else:
        return 'Uncategorized'


def read_level_from_file(filename="results_summary.txt"):
    """Read the difficulty level from a file."""
    try:
        with open(filename, "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        return None


def save_level_to_file(level, filename="results_summary.txt"):
    """Save the difficulty level to a file."""
    try:
        with open(filename, "w") as file:
            file.write(f"{level}\n")
    except Exception as e:
        print(f"Error writing to file: {e}")


def tfidf_similarity(paragraph, question, vectorizer=None):
    """Calculate the cosine similarity between the paragraph and question using TF-IDF."""
    if vectorizer is None:
        vectorizer = TfidfVectorizer()

    # Transform the paragraph and question into vectors
    vectors = vectorizer.fit_transform([paragraph, question])

    # Compute the similarity matrix
    similarity_matrix = cosine_similarity(vectors)

    # Return the similarity score between 0 and 1
    return similarity_matrix[0, 1]
