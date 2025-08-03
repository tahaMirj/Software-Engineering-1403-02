# --- Mock objects to simulate your models ---

class MockChoice:
    def __init__(self, id, label, text, is_correct=False):
        self.id = id
        self.label = label
        self.text = text
        self.is_correct = is_correct

class MockChoicesManager(list):
    def all(self):
        return self

class MockQuestion:
    def __init__(self, text, choices):
        self.text = text
        self.choices = MockChoicesManager(choices)

class MockQuizQuestion:
    def __init__(self, question, user_answer):
        self.question = question
        self.user_answer = user_answer

# --- Sample Data ---
choices_q1 = [
    MockChoice(1, "A", "I goes to school.", is_correct=False),
    MockChoice(2, "B", "I go to school.", is_correct=True),
    MockChoice(3, "C", "I going to school.", is_correct=False),
]

question1 = MockQuestion("Which sentence is correct?", choices_q1)
quiz_question1 = MockQuizQuestion(question1, user_answer=1)  # User chose A (wrong)

incorrect_questions = [quiz_question1]

# --- Test the AI function ---
from ai import generate_feedback_from_api

api_key = "tpsg-z2NijAI5tE2pUSLpFFppFPSChCGavaA"

feedback = generate_feedback_from_api(incorrect_questions, api_key)
print("AI Feedback:", feedback)
