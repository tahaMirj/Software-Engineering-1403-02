import requests
import json

def generate_feedback_from_api(incorrect_questions, api_key):
    prompt = "You are an English teacher. Analyze the student's mistakes and give them feedback.\n\n"

    for i, q in enumerate(incorrect_questions, start=1):
        question = q.question
        choices = question.choices.all()
        correct_choice = next((c for c in choices if c.is_correct), None)
        selected_choice = next((c for c in choices if str(c.id) == str(q.user_answer)), None)

        prompt += f"{i}. Question: {question.text}\n"
        prompt += "   Choices:\n"
        for c in choices:
            prompt += f"     {c.label}. {c.text}"
            if c.is_correct:
                prompt += " ✅"
            prompt += "\n"
        if selected_choice:
            prompt += f"   Student answered: {selected_choice.label}. {selected_choice.text} ❌\n\n"
        else:
            prompt += "   Student did not answer.\n\n"

    prompt += "Please give personalized feedback to the student."

    url = "https://api.metisai.ir/api/v1/chat/openai_chat_completion/completions"
    headers = {
        "Content-Type": "application/json",
        "x-api-key": api_key,
    }

    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": "You are a helpful English teacher."},
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    response_data = response.json()

    content = response_data['choices'][0]['message']['content']
    return content
