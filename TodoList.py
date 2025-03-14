import streamlit as st
import json
import os
from datetime import date
from PIL import Image


tab1,tab2=st.tabs(['AI Powered To-Do List','Handwriting Text Extraction'])
def load_user_data(user):
    file_name = f"tasks_data_{user}.json"
    if os.path.exists(file_name):
        with open(file_name, "r") as file:
            return json.load(file)
    else:
        return {"tasks": [], "dates": []}


def save_user_data(user, data):
    file_name = f"{user}.json"
    with open(file_name, "w") as file:
        json.dump(data, file)

st.title("AI Powered To Do List ")
st.write("Manage your tasks and extract text from handwritten images using this app!")



username=shortuuid.uuid()
with tab1: 
    user_data = load_user_data(username)

    st.subheader("To Do List")

    # Task input section
    col1, col2 = st.columns(2)
    with col1:
        todoinput = st.text_input("Enter a task:")
    with col2:
        deadline = st.date_input("Enter the deadline", value=date.today())

    if st.button("Add Task"):
        if todoinput and todoinput not in user_data["tasks"]:
            user_data["tasks"].append(todoinput)
            user_data["dates"].append(str(deadline))
            save_user_data(username, user_data)
            st.rerun()

    while task_index < len(user_data["tasks"]):
        col1, col2, col3 = st.columns([2, 1, 1])

        with col1:
            st.write(user_data["tasks"][task_index])
        with col3:
            st.write(user_data["dates"][task_index])
        with col2:
            if st.button("Remove", key=f"remove_{task_index}"):
                user_data["tasks"].pop(task_index)
                user_data["dates"].pop(task_index)
                save_user_data(username, user_data)
                st.rerun()

        task_index += 1

with tab2:  
    st.title("Handwriting Text Extraction")
    st.write("Upload an image to extract text (including handwritten text):")
    uploaded_image = st.camera_input("Take a picture")
    if uploaded_image:
        img = Image.open(uploaded_image)
        st.image(img, caption="Uploaded Image", use_column_width=True)

        # Handwriting extraction placeholder logic
        st.write("Extracted Text:")
        st.text("This is where the extracted text will appear. Replace this with your AI model logic for handwriting recognition.")






