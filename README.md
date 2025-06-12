# AI Persona Agent with Quality Control

## Overview
This project implements an AI agent that can represent a person based on their LinkedIn profile and a personal summary. The agent uses a dual-model approach for quality control: OpenAI generates responses, and Google's Gemini evaluates them for quality and accuracy. If a response doesn't meet quality standards, the system automatically regenerates it with feedback.

## Features
- **Personalized AI Representation**: Creates a digital twin based on your LinkedIn profile and personal summary
- **Dual-Model Quality Control**: Uses OpenAI for generation and Gemini for evaluation
- **Feedback Loop**: Automatically improves responses that don't meet quality standards
- **Special Handling**: Includes fun features like responding in Gibberish for patent-related questions
- **User-Friendly Interface**: Provides a chat interface using Gradio

## How It Works
1. **Initial Response Generation**: When a user asks a question, OpenAI generates a response based on the provided LinkedIn profile and summary
2. **Quality Evaluation**: Gemini evaluates the response for accuracy, professionalism, and alignment with the provided context
3. **Feedback Loop**: If the response is rejected, OpenAI receives the feedback and generates an improved response
4. **Final Output**: The approved response is presented to the user through the Gradio interface

## Technical Architecture
- **OpenAI API**: Handles response generation using gpt-4o-mini
- **Google Gemini API**: Evaluates response quality using gemini-2.0-flash
- **Pydantic**: Provides structured data validation for evaluation results
- **PyPDF**: Extracts text from LinkedIn profile PDF
- **Gradio**: Creates an interactive chat interface

## Setup Instructions

### Prerequisites
- Python 3.7+
- OpenAI API key
- Google API key (for Gemini access)

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/rohithsiddi/ai-persona-agent.git
   cd ai-persona-agent
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file with your API keys:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   GOOGLE_API_KEY=your_google_api_key_here
   ```

4. Set up your personal data:
   - Export your LinkedIn profile as PDF and save it as `me/linkedin.pdf`
   - Create a personal summary in `me/summary.txt`

### Usage
Run the application:
```bash
python app.py
```

This will launch a Gradio web interface where users can chat with your AI representative.

## Customization
- **Personal Information**: Update the LinkedIn PDF and summary text with your own information
- **Name**: Change the `name` variable in the `load_profile_data()` function
- **System Prompts**: Modify the prompts to change how your AI representative behaves
- **Models**: Adjust which models are used by changing the model parameters in the API calls

## Requirements
- python-dotenv==1.0.0
- openai==1.3.0
- pypdf==3.17.1
- gradio==4.19.2
- pydantic==2.5.2

## Future Improvements
- Add support for multiple profiles
- Add more specialized handling for different types of questions
- Improve evaluation criteria for different contexts
- Add visualization of the evaluation process
