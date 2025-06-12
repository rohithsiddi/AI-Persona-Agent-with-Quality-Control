from dotenv import load_dotenv
from openai import OpenAI
from pypdf import PdfReader
import gradio as gr
import os
from pydantic import BaseModel

# Load environment variables
load_dotenv(override=True)
openai = OpenAI()

# Initialize Gemini client
gemini = OpenAI(
    api_key=os.getenv("GOOGLE_API_KEY"), 
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Read PDF and summary
def load_profile_data():
    # Read PDF
    reader = PdfReader("me/linkedin.pdf")
    linkedin = ""
    for page in reader.pages:
        text = page.extract_text()
        if text:
            linkedin += text
    
    # Read summary
    with open("me/summary.txt", "r", encoding="utf-8") as f:
        summary = f.read()
    
    # Get name (customize this)
    name = "Rohith Siddi"  # Replace with your name or make this configurable
    
    return linkedin, summary, name

# Evaluation model
class Evaluation(BaseModel):
    is_acceptable: bool
    feedback: str

# Load profile data
linkedin, summary, name = load_profile_data()

# Create prompts
system_prompt = f"""You are acting as {name}. You are answering questions on {name}'s website, \
particularly questions related to {name}'s career, background, skills and experience. \
Your responsibility is to represent {name} for interactions on the website as faithfully as possible. \
You are given a summary of {name}'s background and LinkedIn profile which you can use to answer questions. \
Be professional and engaging, as if talking to a potential client or future employer who came across the website. \
If you don't know the answer, say so.

## Summary:
{summary}

## LinkedIn Profile:
{linkedin}

With this context, please chat with the user, always staying in character as {name}."""

evaluator_system_prompt = f"""You are an evaluator that decides whether a response to a question is acceptable. \
You are provided with a conversation between a User and an Agent. Your task is to decide whether the Agent's latest response is acceptable quality. \
The Agent is playing the role of {name} and is representing {name} on their website. \
The Agent has been instructed to be professional and engaging, as if talking to a potential client or future employer who came across the website. \
The Agent has been provided with context on {name} in the form of their summary and LinkedIn details. Here's the information:

## Summary:
{summary}

## LinkedIn Profile:
{linkedin}

With this context, please evaluate the latest response, replying with whether the response is acceptable and your feedback."""

def evaluator_user_prompt(reply, message, history):
    user_prompt = f"Here's the conversation between the User and the Agent: \n\n{history}\n\n"
    user_prompt += f"Here's the latest message from the User: \n\n{message}\n\n"
    user_prompt += f"Here's the latest response from the Agent: \n\n{reply}\n\n"
    user_prompt += f"Please evaluate the response, replying with whether it is acceptable and your feedback."
    return user_prompt

def evaluate(reply, message, history) -> Evaluation:
    messages = [
        {"role": "system", "content": evaluator_system_prompt},
        {"role": "user", "content": evaluator_user_prompt(reply, message, history)}
    ]
    response = gemini.beta.chat.completions.parse(
        model="gemini-2.0-flash", 
        messages=messages, 
        response_format=Evaluation
    )
    return response.choices[0].message.parsed

def rerun(reply, message, history, feedback):
    updated_system_prompt = system_prompt + f"\n\n## Previous answer rejected\nYou just tried to reply, but the quality control rejected your reply\n"
    updated_system_prompt += f"## Your attempted answer:\n{reply}\n\n"
    updated_system_prompt += f"## Reason for rejection:\n{feedback}\n\n"
    messages = [{"role": "system", "content": updated_system_prompt}] + history + [{"role": "user", "content": message}]
    response = openai.chat.completions.create(model="gpt-4o-mini", messages=messages)
    return response.choices[0].message.content

def chat(message, history):
    # Special case for patent questions
    if "patent" in message:
        system = system_prompt + "\n\nEverything in your reply needs to be in Gibberish - \
              it is mandatory that you respond only and entirely in Gibberish (insert 'idig' after every consonant sound or use a consistent gibberish rule throughout)."

    else:
        system = system_prompt
    
    # Get initial response from OpenAI
    messages = [{"role": "system", "content": system}] + history + [{"role": "user", "content": message}]
    response = openai.chat.completions.create(model="gpt-4o-mini", messages=messages)
    reply = response.choices[0].message.content

    # Evaluate the response using Gemini
    evaluation = evaluate(reply, message, history)
    
    # If not acceptable, rerun with feedback
    if evaluation.is_acceptable:
        print("Passed evaluation - returning reply")
    else:
        print("Failed evaluation - retrying")
        print(evaluation.feedback)
        reply = rerun(reply, message, history, evaluation.feedback)
    
    return reply

# Launch Gradio interface
if __name__ == "__main__":
    gr.ChatInterface(chat, type="messages").launch() 