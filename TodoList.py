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
genai.configure(api_key="YOUR_API_KEY")  # Replace with your actual API key
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

    todoinput = st.text_input("Enter a task:")
    deadline = st.date_input("Enter the deadline")

    if st.button("Add Task"):
        user = json.dumps(userdata)
        userdata = json.loads(user)

        task = todoinput
        userdata["tasks"].append({"task": task, "deadline": str(deadline)})
        with open(user, "w") as file:
            json.dump(userdata, file)
        st.rerun()

    user = json.dumps(userdata)
    userdata = json.loads(user)

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
                    f'Break down the following task: {task_data["task"]} into chunks that can be completed in sessions. '
                    'Split it into stages, so Stage 1: Do this, Stage 2: Do this, and so on for 10 stages. '
                    'Each stage must have max. 20 words. Keep it all the same font. Add a new line before every stage. '
                    'However, if a task is given, you must break it down. Like you need to. Even if it is a repeat task, you need to. No matter what, break down the task. Don\'t repeat the prompt in your response exactly.'
                )
                st.session_state.responses[task_data['task']] = response.text
            except ResourceExhausted:
                st.error("API quota exceeded. Please try again later or increase your quota.")
                st.session_state.responses[task_data['task']] = "API Quota Exceeded. Please try again later"

        st.text_area(f'AI Task Breakdown:', st.session_state.responses[task_data['task']], height=200)

        with col2:
            if st.button("Remove", key=f"remove_{i}"):
                userdata["tasks"].pop(i)
                if task_data['task'] in st.session_state.responses:
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
        except ResourceExhausted:
            st.error("API quota exceeded. Please try again later or increase your quota.")
