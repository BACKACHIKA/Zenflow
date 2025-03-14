import streamlit as st
import google.generativeai as genai
import shortuuid
from PIL import Image
import json
import os

# Configure Generative AI
genai.configure(api_key="AIzaSyBEnO9-HQgK4dVACYvYmJCJ58L_kh4lJ1I")
model = genai.GenerativeModel("gemini-1.5-flash")

# Filepath for storing data
data_file = "tasks_data.json"

# Load data from JSON file
def load_data():
    if os.path.exists(data_file):
        with open(data_file, "r") as file:
            return json.load(file)
    else:
        return {"tasks": [], "dates": []}

# Save data to JSON file
def save_data(data):
    with open(data_file, "w") as file:
        json.dump(data, file)

# Initialize data
data = load_data()

tab1, tab2 = st.tabs(['AI Powered To Do List', 'Handwriting Text Extraction'])

with tab1:
    st.title('To Do List')
    st.write(
        'This is a to-do list app that uses AI to break down your tasks into simple, manageable sub-tasks.')

    col1, col2 = st.columns(2)

    with col1:
        todoinput = st.text_input('Enter a task:')

    with col2:
        date = st.date_input('Enter the deadline')

    if st.button('Add Task'):
        if todoinput and todoinput not in data["tasks"]:
            data["tasks"].append(todoinput)
            data["dates"].append(str(date))
            save_data(data)
            st.experimental_rerun()

    def remove_task(task_index):
        data["tasks"].pop(task_index)
        data["dates"].pop(task_index)
        save_data(data)
        st.experimental_rerun()

    for task_index, task in enumerate(data["tasks"]):
        col1, col2, col3 = st.columns([2, 1, 1])

        with col1:
            st.write(task)

        with col3:
            st.write(data["dates"][task_index])

        with col2:
            if st.button('Remove', key='Remove' + str(task_index)):
                remove_task(task_index)

        response = model.generate_content(
            f'Break down the following task: {task} into chunks that can be completed in sessions. '
            'Split it into stages, so Stage 1: Do this, Stage 2: Do this, and so on for 10 stages. '
            'Each stage must have max. 20 words. Keep it all the same font. Add a new line before every stage. '
            'However if a task is given, you must break it down. Even if it’s a repeat task, break it down.'
        )
        st.text_area(f'AI Task Breakdown for: {task}', response.text, height=200)

with tab2:
    st.title('Image to Text')
    st.write('This is an AI-powered tool that extracts text from an image (including handwritten text).')

    text = st.camera_input('Take a picture to scan:')

    if text:
        img = Image.open(text)

        responses = model.generate_content(contents=["What text is written in the image?", img])
        st.write(responses.text)




