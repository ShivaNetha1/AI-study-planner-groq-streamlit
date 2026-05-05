# AI Study Planner

A simple and interactive web application built with Streamlit and powered by Groq's LLaMA 3.3 model. This app helps users generate detailed, customized study plans based on their specific goals, available days, and daily study hours.

## Features

* **Customizable Study Goals**: Input whatever you want to learn.
* **Flexible Scheduling**: Set the number of days and hours per day you want to dedicate to studying.
* **AI-Powered Generation**: Uses the fast and powerful `llama-3.3-70b-versatile` model via the Groq API to create detailed, day-by-day study topics.

## Prerequisites

* Python 3.8+
* A Groq API Key

## Installation

1. **Navigate to the project directory**.
2. **Create a virtual environment**:
   ```bash
   python -m venv .venv
   ```
3. **Activate the virtual environment**:
   * On Windows: `.venv\Scripts\activate`
   * On macOS/Linux: `source .venv/bin/activate`
4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
5. **Set up environment variables**:
   Create a `.env` file in the root directory of the project and add your Groq API key:
   ```env
   GROQ_API_KEY=your_actual_api_key_here
   ```

## Usage

To start the application, run the following command in your terminal:

```bash
streamlit run main.py
```