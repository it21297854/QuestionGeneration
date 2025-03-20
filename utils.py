from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def categorize_difficulty(paragraph, keywords):
    """Categorize difficulty based on keyword presence and paragraph length."""
    print(f"\nChecking difficulty for paragraph: {paragraph[:100]}...")

    paragraph_lower = paragraph.lower()
    length = len(paragraph)

    # Count keyword occurrences for each level
    high_level_count = sum(paragraph_lower.count(keyword) for keyword in keywords['high_level'])
    medium_level_count = sum(paragraph_lower.count(keyword) for keyword in keywords['medium_level'])
    low_level_count = sum(paragraph_lower.count(keyword) for keyword in keywords['low_level'])

    # Debugging output
    print(f"Keyword Matches - High: {high_level_count}, Medium: {medium_level_count}, Low: {low_level_count}")
    print(f"Paragraph Length: {length}")

    # Determine difficulty based on keyword frequency and length
    if high_level_count >= 2 or (high_level_count > 0 and length > 500):
        return 'High Level'
    elif medium_level_count >= 2 or (medium_level_count > 0 and length > 300):
        return 'Medium Level'
    elif low_level_count >= 2 or (low_level_count > 0 and length <= 300):
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


# def tfidf_similarity(paragraph, question, vectorizer=None):
#     """Calculate the cosine similarity between the paragraph and question using TF-IDF."""
#     if vectorizer is None:
#         vectorizer = TfidfVectorizer()
#
#     # Transform the paragraph and question into vectors
#     vectors = vectorizer.fit_transform([paragraph, question])
#
#     # Compute the similarity matrix
#     similarity_matrix = cosine_similarity(vectors)
#
#     # Return the similarity score between 0 and 1
#     return similarity_matrix[0, 1]
