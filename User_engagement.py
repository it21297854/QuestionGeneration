import json
from datetime import datetime

# File to store user engagement data
ENGAGEMENT_FILE = "user_engagement.txt"

# Sample questions based on engagement levels
QUESTIONS = {
    "low": "What motivates you to engage more with the platform?",
    "medium": "What features do you find most useful?",
    "high": "Would you recommend this platform to others?"
}

def log_engagement(user_id, activity_type, metadata=None):
    """Log user engagement to a text file."""
    engagement_data = {
        "user_id": user_id,
        "activity_type": activity_type,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "metadata": metadata
    }

    try:
        with open(ENGAGEMENT_FILE, "a") as file:
            file.write(json.dumps(engagement_data) + "\n")
        print("Engagement logged successfully!")
    except Exception as e:
        print(f"Error logging engagement: {e}")

def calculate_engagement_level(percentage):
    """Determine engagement level based on input percentage."""
    if percentage < 40:
        return "low"
    elif 40 <= percentage < 70:
        return "medium"
    else:
        return "high"

def get_question_for_user(percentage):
    """Get a question for the user based on their engagement level."""
    engagement_level = calculate_engagement_level(percentage)
    return QUESTIONS.get(engagement_level, "No question available.")

def read_engagement_logs():
    """Read and display all engagement logs from the text file."""
    try:
        with open(ENGAGEMENT_FILE, "r") as file:
            logs = file.readlines()
            engagement_logs = [json.loads(log.strip()) for log in logs]
            return engagement_logs
    except FileNotFoundError:
        print("No engagement logs found.")
        return []
    except Exception as e:
        print(f"Error reading engagement logs: {e}")
        return []

# Example usage
if __name__ == "__main__":
    # Log some engagement data
    log_engagement(user_id=1, activity_type="answered_question", metadata="Question ID: 101")
    log_engagement(user_id=2, activity_type="viewed_page", metadata="Page: Dashboard")
    log_engagement(user_id=1, activity_type="completed_task", metadata="Task: Profile Update")

    # Get a question for a user with a given engagement percentage
    percentage = float(input("Enter engagement percentage: "))
    question = get_question_for_user(percentage)
    print(f"Question for user: {question}")

    # Display all engagement logs
    print("\nEngagement Logs:")
    logs = read_engagement_logs()
    for log in logs:
        print(log)
