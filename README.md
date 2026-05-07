# AI Study Planner

## Live Demo

[Click here to use the app](https://ai-study-planner-llm.streamlit.app/)

## Overview

AI Study Planner is a beginner-friendly GenAI web application built with Streamlit and powered by the Groq API. It helps learners generate a personalized day-by-day study plan based on their goal, current skill level, available days, daily study hours, preferred learning style, and weak areas.

The project demonstrates basic GenAI app development concepts such as prompt engineering, API integration, environment variable handling, Streamlit forms, session state, error handling, and downloadable AI-generated output.

## Features

- Personalized study plan generation using Groq-hosted LLMs.
- Model selection from the sidebar.
- Skill level selection: Beginner, Intermediate, or Advanced.
- Study style selection:
  - Balanced learning
  - Exam preparation
  - Project-based learning
  - Revision focused
- Optional weak areas or extra focus input.
- Number of study days and hours per day controls.
- Creativity slider to control response variation.
- Response length slider to control output size.
- Clean Markdown output with:
  - Plan summary
  - Day-by-day study table
  - Daily time split
  - Revision checkpoints
  - Mini project or assessment idea
  - Free resource suggestions
  - Motivation and consistency tips
- Session history for previously generated plans.
- Download button to save the plan as a Markdown file.
- API key validation using `.env` or Streamlit secrets.
- Simple error handling for missing keys or failed API calls.

## AI Models Used

The app currently supports the following Groq models:

- `llama-3.3-70b-versatile`
- `qwen/qwen3-32b`
- `llama-3.1-8b-instant`
- `openai/gpt-oss-120b`

## Tech Stack

- Python
- Streamlit
- Groq API
- python-dotenv

## Project Structure

```text
AI-Study-Planner/
|-- main.py
|-- requirements.txt
|-- README.md
|-- .env
`-- .gitignore
```

## Prerequisites

- Python 3.8 or above
- Groq API key

## Installation

1. Clone the repository.

```bash
git clone https://github.com/ShivaNetha1/AI-study-planner-groq-streamlit
cd AI-study-planner-groq-streamlit
```

2. Create a virtual environment.

```bash
python -m venv .venv
```

3. Activate the virtual environment.

Windows:

```bash
.venv\Scripts\activate
```

macOS/Linux:

```bash
source .venv/bin/activate
```

4. Install dependencies.

```bash
pip install -r requirements.txt
```

5. Create a `.env` file in the root directory.

```env
GROQ_API_KEY=your_groq_api_key_here
```

## Usage

Run the Streamlit app:

```bash
streamlit run main.py
```

Then open the local URL shown in your terminal, usually:

```text
http://localhost:8501
```

## How It Works

1. The user enters a learning goal, study duration, daily study hours, and optional weak areas.
2. The user selects model settings such as AI model, skill level, plan style, creativity, and response length.
3. The app builds a structured system prompt and user prompt.
4. The prompt is sent to the Groq chat completions API.
5. The generated study plan is displayed in Markdown.
6. The plan is stored in Streamlit session state and can be downloaded as a Markdown file.

## GenAI Concepts Demonstrated

- LLM API integration
- Prompt engineering
- System and user message separation
- Temperature control
- Token limit control
- Streamlit session state
- Environment variable management
- Basic frontend design with Streamlit
- Error handling and input validation

## Future Improvements

- Add PDF download support.
- Add user login and persistent database storage.
- Add calendar export.
- Add progress tracking for completed study days.
- Add a chatbot mode for follow-up questions about the generated plan.
- Add RAG support to recommend resources from uploaded notes or documents.
