import streamlit as st
import json
import os
from datetime import date
from PIL import Image
import shortuuid
import google.generativeai as genai

st.title("AI Powered To-Do List")
user = f'{shortuuid.uuid()}.json'
genai.configure(api_key="AIzaSyBEnO9-HQgK4dVACYvYmJCJ58L_kh4lJ1I")
model = genai.GenerativeModel("gemini-1.5-flash")


tab1, tab2 = st.tabs(['AI Powered To-Do List', 'Handwriting Text Extraction'])

if os.path.exists(user):
    with open(userdata, "r") as file:
        userdata = json.load(file)
else:
    userdata = {"tasks": [], "dates": []}

with tab1:
    st.subheader("To-Do List")

    col1, col2 = st.columns(2)
    with col1:
        todoinput = st.text_input("Enter a task:")
    with col2:
        deadline = st.date_input("Enter the deadline")


    if st.button("Add Task"):
        
            userdata=userdata["tasks"].append(todoinput)
           
            st.write(userdata)

          
 
    
    for i in range(len(userdata["tasks"])):
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            st.write(userdata["tasks"][i])
        with col3:
            st.write(userdata["dates"][i])
            

        response = model.generate_content(
            f'Break down the following task: {userdata["tasks"][i]} into chunks that can be completed in. sessions. '
            'Split it into stages, so Stage 1: Do this, Stage 2: Do this, and so on for 10 stages. '
            'Each stage must have max. 20 words. Keep it all the same font. Add a new line before every stage. '
            'However if a task is given,you must break it down.Like you need to.Even if its a repeat task,you need to.No matter what break down the task.Don\'t repeat the prompt in your response ever.'
        )
        st.text_area(f'AI Task Breakdown:', response.text, height=200)
        with col2:
            if st.button("Remove", key=f"remove_{i}"):
                userdata["tasks"].pop(i)
                userdata["tasks"].pop(i)
                with open(user, "w") as file:
                    json.dump(user, file)
                st.rerun()

with tab2:
    st.title('Image to Text')
    st.write('This is an AI-powered tool that extracts text from an image (including handwritten text).')

    text = st.camera_input('Take a picture to scan:')

    if text:
        img = Image.open(text)

        responses = model.generate_content(contents=["What text is written in the image?", img])
        st.write(responses.text)







