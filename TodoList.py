import streamlit as st
import json
import os
from datetime import date
from PIL import Image
import shortuuid

# Title
st.title("AI Powered To-Do List")
user = f'{shortuuid.uuid()}.json'

# Tabs
tab1, tab2 = st.tabs(['AI Powered To-Do List', 'Handwriting Text Extraction'])

# User data initialization
if os.path.exists(user):
    with open(user, "r") as file:
        userdata = json.load(file)
else:
    userdata = {"tasks": [], "dates": []}

with tab1:
    st.subheader("To-Do List")

    # Task input section
    col1, col2 = st.columns(2)
    with col1:
        todoinput = st.text_input("Enter a task:")
    with col2:
        deadline = st.date_input("Enter the deadline")

    # Add Task button
    if st.button("Add Task"):
        
            userdata["tasks"].append(todoinput)
            userdata["dates"].append(str(deadline))
            with open(user, "w") as file:
                json.dump(userdata, file)
            st.rerun() 

 
    for i in range(len(userdata["tasks"])):
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            st.write(userdata["tasks"][i])
        with col3:
            st.write(userdata["dates"][i])
        with col2:
            if st.button("Remove", key=f"remove_{i}"):
                userdata["tasks"].pop(i)
                userdata["dates"].pop(i)
                with open(user, "w") as file:
                    json.dump(userdata, file)
                st.experimental_rerun()

with tab2:
    st.title('Image to Text')
    st.write('This is an AI-powered tool that extracts text from an image (including handwritten text).')

    text = st.camera_input('Take a picture to scan:')

    if text:
        img = Image.open(text)

        responses = model.generate_content(contents=["What text is written in the image?", img])
        st.write(responses.text)







