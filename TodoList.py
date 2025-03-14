import streamlit as st
import json
import os
from datetime import date

# Function to load user-specific data from a JSON file
def load_user_data(user):
    file_name = f"tasks_data_{user}.json"
    if os.path.exists(file_name):
        with open(file_name, "r") as file:
            return json.load(file)
    else:
        return {"tasks": [], "dates": []}

# Function to save user-specific data to a JSON file
def save_user_data(user, data):
    file_name = f"tasks_data_{user}.json"
    with open(file_name, "w") as file:
        json.dump(data, file)

# Sidebar: User Login
st.sidebar.title("User Login")
user = st.sidebar.text_input("Enter your username:", placeholder="Type your name here")

if user:
    st.sidebar.success(f"Logged in as {user}")
    user_data = load_user_data(user)

    st.title("AI Powered To Do List")
    st.write("This is a to-do list app that uses AI and stores tasks locally for each user.")

    # Task input
    col1, col2 = st.columns(2)

    with col1:
        todoinput = st.text_input("Enter a task:")

    with col2:
        deadline = st.date_input("Enter the deadline", value=date.today())

    if st.button("Add Task"):
        if todoinput and todoinput not in user_data["tasks"]:
            user_data["tasks"].append(todoinput)
            user_data["dates"].append(str(deadline))
            save_user_data(user, user_data)
            st.experimental_rerun()

    # Display tasks
    for i, task in enumerate(user_data["tasks"]):
        col1, col2, col3 = st.columns([2, 1, 1])

        with col1:
            st.write(task)
        with col3:
            st.write(user_data["dates"][i])

        with col2:
            if st.button("Remove", key=f"remove_{i}"):
                user_data["tasks"].pop(i)
                user_data["dates"].pop(i)
                save_user_data(user, user_data)
                st.experimental_rerun()
else:
    st.warning("Please enter your username to access your tasks.")




