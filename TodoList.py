import streamlit as st
import google.generativeai as genai
import json
from PIL import Image
import os

genai.configure(api_key="AIzaSyCjwfeub06TqcY2D5rgUiKwaX57BXywo5E")
model = genai.GenerativeModel("gemini-1.5-flash")

# Function to save tasks to JSON
def save_tasks(tasks, dates):
    data = {"tasks": tasks, "dates": [date.isoformat() for date in dates]}
    try:
        with open("tasks.json", "w") as f:
            json.dump(data, f)
    except Exception as e:
        st.error(f"Error saving tasks: {e}")

# Function to load tasks from JSON
def load_tasks():
    if os.path.exists("tasks.json"):
        try:
            with open("tasks.json", "r") as f:
                data = json.load(f)
                return data["tasks"], [st.session_state.get_date(date_str) for date_str in data["dates"]]
        except Exception as e:
            st.error(f"Error loading tasks: {e}")
            return [], []
    else:
        return [], []

# Custom widget to convert date string to date object.
def get_date(date_str):
    from datetime import datetime
    return datetime.strptime(date_str, "%Y-%m-%d").date()

# Add get_date to session state so it can be used in load_tasks.
if 'get_date' not in st.session_state:
    st.session_state.get_date = get_date

tab1, tab2 = st.tabs(['AI Powered To Do list', 'Handwriting Text Extraction'])

with tab1:
    st.title('To Do List')
    st.write(
        'This is a to-do list app that uses AI to break down your tasks into simple, manageable sub-tasks.')

    if 'tasks' not in st.session_state:
        st.session_state.tasks, st.session_state.dates = load_tasks()

    col1, col2 = st.columns(2)

    with col1:
        todoinput = st.text_input('Enter a task:')

    with col2:
        date = st.date_input('Enter the deadline')

    if st.button('Add Task'):
        if todoinput and todoinput not in st.session_state.tasks:
            st.session_state.tasks.append(todoinput)
            st.session_state.dates.append(date)
            save_tasks(st.session_state.tasks, st.session_state.dates)
            # st.rerun() #removed st.rerun()

    def remove_task(task_index):
        st.session_state.tasks.pop(task_index)
        st.session_state.dates.pop(task_index)
        save_tasks(st.session_state.tasks, st.session_state.dates)
        st.rerun()

    for task_index in range(len(st.session_state.tasks)):
        col1, col2, col3 = st.columns([2, 1, 1])

        with col2:
            if st.button('Remove', key=f'Remove{task_index}'):
                remove_task(task_index)

        with col1:
            st.write(st.session_state.tasks[task_index])
        with col3:
            st.write(st.session_state.dates[task_index])

        response = model.generate_content(
            f'Break down the following task: {st.session_state.tasks[task_index]} into chunks that can be completed in sessions. '
            'Split it into stages, so Stage 1: Do this, Stage 2: Do this, and so on for 10 stages. '
            'Each stage must have max. 20 words. Keep it all the same font. Add a new line before every stage. '
            'However if a task is given,you must break it down.Like you need to.Even if its a repeat task,you need to.No matter what break down the task.'
        )
        st.text_area(f'AI Task Breakdown for: {st.session_state.tasks[task_index]}', response.text, height=200)

with tab2:
    st.title('Image to Text')
    st.write('This is an AI-powered tool that extracts text from an image (including handwritten text).')

    text = st.camera_input('Take a picture to scan:')

    if text:
        img = Image.open(text)

        responses = model.generate_content(contents=["What text is written in the image?", img])
        st.write(responses.text)
