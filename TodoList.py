import streamlit as st
import json
import os
from datetime import date
from PIL import Image
import shortuuid
import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted

st.title("AI Powered To-Do List")
user = f'{shortuuid.uuid()}.json'
genai.configure(api_key="AIzaSyBEnO9-HQgK4dVACYvYmJCJ58L_kh4lJ1I")  # Replace with your actual API key
model = genai.GenerativeModel("gemini-1.5-flash")

tab1, tab2 = st.tabs(['AI Powered To-Do List', 'Handwriting Text Extraction'])

if os.path.exists(user):
    with open(user, "r") as file:
        try:
            userdata = json.load(file)
        except json.JSONDecodeError:
            userdata = {"tasks": []}
else:
    userdata = {"tasks": []}

with tab1:
    st.subheader("To-Do List")

    col1, col2 = st.columns(2)
    with col1:
        todoinput = st.text_input("Enter a task:")
    with col2:
        deadline = st.date_input("Enter the deadline")

    if st.button("Add Task"):
        if todoinput:
            task = todoinput.strip()
            if task:
                userdata["tasks"].append({"task": task, "deadline": str(deadline)})
                with open(user, "w") as file:
                    json.dump(userdata, file)
                st.rerun()

    for i in range(len(userdata["tasks"])):
        task_data = userdata["tasks"][i]
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            st.write(f"{task_data['task']} (Deadline: {task_data['deadline']})")

        if 'responses' not in st.session_state:
            st.session_state.responses = {}

        if task_data['task'] not in st.session_state.responses:
            try:
                response = model.generate_content(
                    prompt=f'Break down the following task: {task_data["task"]} into chunks that can be completed in sessions. '
                           'Split it into stages, so Stage 1: Do this, Stage 2: Do this, and so on for 10 stages. '
                           'Each stage must have max. 20 words. Keep it all the same font. Add a new line before every stage. '
                           'However, if a task is given, you must break it down. Like you need to. Even if it is a repeat task, you need to. No matter what, break down the task. Don\'t repeat the prompt in your response exactly.'
                )
                st.session_state.responses[task_data['task']] = response.text
                # Add a delay to prevent too many requests at once
                time.sleep(1)
            except ResourceExhausted:
                st.error("API quota exceeded. Please try again later or increase your quota.")
                break

        st.text_area(f'AI Task Breakdown:', st.session_state.responses[task_data['task']], height=200)

        with col2:
            if st.button("Remove", key=f"remove_{i}"):
                userdata["tasks"].pop(i)
                del st.session_state.responses[task_data['task']]
                with open(user, "w") as file:
                    json.dump(userdata, file)
                st.rerun()

with tab2:
    st.title('Image to Text')
    st.write('This is an AI-powered tool that extracts text from an image (including handwritten text).')

    text = st.camera_input('Take a picture to scan:')

    if text:
        img = Image.open(text)
        try:
            responses = model.generate_content(contents=["What text is written in the image?", img])
            st.write(responses.text)
            # Add a delay to prevent too many requests at once
            time.sleep(1)
        except ResourceExhausted:
            st.error("API quota exceeded. Please try again later or increase your quota.")