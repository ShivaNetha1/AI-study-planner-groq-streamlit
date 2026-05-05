# ai agent with py st & grok
# for study planner:
import streamlit as st
from groq import Groq
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()


client = Groq(api_key=os.getenv("GROQ_API_KEY"))

st.title('Study Planner')
st.write('Welcome to the Study Planner! Please enter your study goals and schedule below.')
# st.text_input('What subjects do you want to study?')
# st.text_input('How many hours per day do you want to study?')
goal=st.text_input('what your goal?')
days=st.number_input('how many days do you want to study?', min_value=1, step=1)
hours=st.number_input('how many hours per day do you want to study?', min_value=1, step=1)  


def fetch_plan(goal, days, hours):
    p=f'""" create a study plan for the following goal: {goal}. ' \
    f'The plan should include a schedule for studying for {hours} hours per day for {days} days. ' \
    f'The plan should be detailed and include specific topics to study each day. """'

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile", 
            messages=[{"role": "user", "content": p}])
        st.write(response.choices[0].message.content)
    except Exception as e:
        st.error(f"Error fetching study plan: {e}")

if st.button('Generate Study Plan'):
    if goal:
        with st.spinner('Generating study plan...'):
            fetch_plan(goal, days, hours)
            st.success(f'Your study plan for {goal} is to study for {hours} hours per day for {days} days.')
    else:
        st.warning('Please fill in all the fields.')
