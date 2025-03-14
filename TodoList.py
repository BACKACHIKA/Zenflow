import streamlit as st
import json
import os
from datetime import date
from PIL import Image
import shortuuid
st.title("AI Powered To Do List ")
taskindex=0
user=f'{shortuuid.uuid()}.json'

tab1,tab2=st.tabs(['AI Powered To-Do List','Handwriting Text Extraction'])
file_name = f"{user}.json"
    
if os.path.exists(user):
    with open(user, "r") as file:
        userdata=json.load(user)
else:
    userdata={"tasks": [], "dates": []}



user=json.dumps(str(userdata))





username=shortuuid.uuid()
with tab1: 
    

    st.subheader("To Do List")

    # Task input section
    col1, col2 = st.columns(2)
    with col1:
        todoinput = st.text_input("Enter a task:")
    with col2:
        deadline = st.date_input("Enter the deadline")

    if st.button("Add Task"):
        
        userdata["tasks"].append(todoinput)
        userdata["dates"].append(str(deadline))
        with open(user, "w") as file:
             user=json.dumps(userdata)        
            

             st.rerun()

for i in range(len(userdata["tasks"])):
        col1, col2, col3 = st.columns([2, 1, 1])

        with col1:
            st.write(user_data["tasks"][i])
            print(user_data["tasks"][i])(user_data["tasks"][i])
        with col3:
            st.write(user_data["dates"][i])
        with col2:
            if st.button("Remove", key=f"remove_{task_index}"):
                user_data["tasks"].pop(task_index)
                user_data["dates"].pop(task_index)
                save_user_data(username, user_data)
                st.rerun()


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






