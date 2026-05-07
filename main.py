import os
from datetime import datetime

import streamlit as st
from dotenv import load_dotenv
from groq import Groq


load_dotenv()


MODEL_OPTIONS = {
    "Llama 3.3 70B Versatile": "llama-3.3-70b-versatile",
    "Qwen 3 32B": "qwen/qwen3-32b",
    "Llama 3.1 8B Instant": "llama-3.1-8b-instant",
    "GPT OSS 120B": "openai/gpt-oss-120b",
}

LEVEL_OPTIONS = ["Beginner", "Intermediate", "Advanced"]
STYLE_OPTIONS = [
    "Balanced learning",
    "Exam preparation",
    "Project-based learning",
    "Revision focused",
]


st.set_page_config(
    page_title="AI Study Planner",
    layout="wide",
)


def get_api_key():
    try:
        secret_key = st.secrets.get("GROQ_API_KEY")
    except Exception:
        secret_key = None

    return secret_key or os.getenv("GROQ_API_KEY")


def create_groq_client(api_key):
    return Groq(api_key=api_key)


def build_messages(goal, days, hours, level, learning_style, weak_areas):
    system_prompt = """
You are an AI study coach. Create practical, realistic study plans.
Return the answer in clean Markdown.
Do not invent paid courses, exact URLs, or fake certifications.
Make the plan beginner-friendly when the selected level is Beginner.
"""

    user_prompt = f"""
Create a study plan using the following details:

Goal: {goal}
Skill level: {level}
Total days: {days}
Study hours per day: {hours}
Preferred plan style: {learning_style}
Weak areas or extra focus: {weak_areas if weak_areas else "None mentioned"}

The response must include:
1. A short plan summary.
2. A day-by-day table with Day, Topics, Practice Task, and Output.
3. A daily time split for {hours} hour(s).
4. Revision checkpoints.
5. Mini project or assessment idea.
6. Simple free resource suggestions without fake links.
7. Motivation and consistency tips.

Keep the plan realistic and specific.
"""

    return [
        {"role": "system", "content": system_prompt.strip()},
        {"role": "user", "content": user_prompt.strip()},
    ]


def generate_study_plan(model, messages, temperature, max_tokens):
    api_key = get_api_key()

    if not api_key:
        raise ValueError(
            "GROQ_API_KEY is missing. Add it to a .env file or Streamlit secrets."
        )

    client = create_groq_client(api_key)
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return response.choices[0].message.content


def save_to_history(goal, plan, model, days, hours, level):
    st.session_state.history.insert(
        0,
        {
            "goal": goal,
            "plan": plan,
            "model": model,
            "days": days,
            "hours": hours,
            "level": level,
            "created_at": datetime.now().strftime("%d %b %Y, %I:%M %p"),
        },
    )


if "history" not in st.session_state:
    st.session_state.history = []

if "latest_plan" not in st.session_state:
    st.session_state.latest_plan = ""


st.title("AI Study Planner")
st.caption("Generate a clear day-by-day study plan using Groq and Streamlit.")

with st.sidebar:
    st.header("Settings")

    selected_model_name = st.selectbox(
        "AI model",
        options=list(MODEL_OPTIONS.keys()),
        index=0,
    )
    selected_model = MODEL_OPTIONS[selected_model_name]

    level = st.radio("Skill level", LEVEL_OPTIONS, horizontal=False)
    learning_style = st.selectbox("Plan style", STYLE_OPTIONS)

    st.divider()
    temperature = st.slider(
        "Creativity",
        min_value=0.0,
        max_value=1.0,
        value=0.4,
        step=0.1,
        help="Lower values make the plan more focused. Higher values make it more creative.",
    )
    max_tokens = st.slider(
        "Response length",
        min_value=800,
        max_value=4000,
        value=2000,
        step=200,
    )

    st.divider()
    if get_api_key():
        st.success("Groq API key loaded")
    else:
        st.warning("Add GROQ_API_KEY to .env or Streamlit secrets")


with st.form("study_plan_form"):
    st.subheader("Study details")

    goal = st.text_area(
        "What do you want to learn?",
        placeholder="Example: Learn Python and GenAI basics to build a chatbot project",
        height=100,
    )

    weak_areas = st.text_input(
        "Weak areas or extra focus",
        placeholder="Example: prompting, APIs, Python basics, deployment",
    )

    days_col, hours_col = st.columns(2)
    with days_col:
        days = st.number_input(
            "Number of days",
            min_value=1,
            max_value=180,
            value=14,
            step=1,
        )
    with hours_col:
        hours = st.number_input(
            "Hours per day",
            min_value=1,
            max_value=12,
            value=2,
            step=1,
        )

    submitted = st.form_submit_button("Generate study plan", type="primary")


if submitted:
    clean_goal = goal.strip()

    if not clean_goal:
        st.warning("Please enter a study goal.")
    elif len(clean_goal) < 10:
        st.warning("Please describe your goal in a little more detail.")
    else:
        messages = build_messages(
            goal=clean_goal,
            days=days,
            hours=hours,
            level=level,
            learning_style=learning_style,
            weak_areas=weak_areas.strip(),
        )

        try:
            with st.spinner("Creating your personalized study plan..."):
                plan = generate_study_plan(
                    model=selected_model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens,
                )

            st.session_state.latest_plan = plan
            save_to_history(
                goal=clean_goal,
                plan=plan,
                model=selected_model,
                days=days,
                hours=hours,
                level=level,
            )
            st.success("Study plan generated successfully.")

        except ValueError as error:
            st.error(str(error))
        except Exception as error:
            st.error(f"Unable to generate the study plan: {error}")


if st.session_state.latest_plan:
    st.divider()
    st.subheader("Generated study plan")
    st.markdown(st.session_state.latest_plan)

    st.download_button(
        label="Download plan as Markdown",
        data=st.session_state.latest_plan,
        file_name="study_plan.md",
        mime="text/markdown",
    )


if st.session_state.history:
    st.divider()
    history_title_col, clear_col = st.columns([3, 1])
    with history_title_col:
        st.subheader("Previous plans")
    with clear_col:
        if st.button("Clear history"):
            st.session_state.history = []
            st.session_state.latest_plan = ""
            st.rerun()

    for index, item in enumerate(st.session_state.history, start=1):
        title = f"{index}. {item['goal']} - {item['created_at']}"
        with st.expander(title):
            st.write(
                f"Model: `{item['model']}` | Level: `{item['level']}` | "
                f"Duration: `{item['days']} days`, `{item['hours']} hours/day`"
            )
            st.markdown(item["plan"])
