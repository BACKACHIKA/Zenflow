import streamlit as st
import google.generativeai as genai
import shortuuid
from PIL import Image

# Configure AI Model once
genai.configure(api_key="AIzaSyBEnO9-HQgK4dVACYvYmJCJ58L_kh4lJ1I")
model = genai.GenerativeModel("gemini-1.5-flash")

st.sidebar.title('Choose a tool:')
page = st.sidebar.selectbox('Go to', ('To Do List', 'AI Text Extraction'))

if page == 'To Do List':
    st.title('To Do List')
    st.sidebar.write('This is a to-do list app that uses AI to break down your tasks into simple, manageable sub-tasks.')

    if 'tasks' not in st.session_state:
        st.session_state.tasks = []
    if 'dates' not in st.session_state:
        st.session_state.dates = []
    if 'ai_breakdowns' not in st.session_state:
        st.session_state.ai_breakdowns = {}

    col1, col2 = st.columns(2)

    with col1:
        todoinput = st.text_input('Enter a task:')
    
    with col2:
        date = st.date_input('Enter the deadline')

    if st.button('Add Task'):
        if todoinput and todoinput not in st.session_state.tasks:
            st.session_state.tasks.append(todoinput)
            st.session_state.dates.append(date)

            # Generate AI breakdown before rerunning
            response = model.generate_content(
                f'Break down the following task: {todoinput} into chunks that can be completed in pomodoro sessions. '
                'Split it into stages, so Stage 1: Do this, Stage 2: Do this, and so on for 10 stages. '
                'Each stage must have max. 20 words. Keep it all the same font. Add a new line before every stage. '
                'If no task is given, say Please enter a task above.'
            )
            st.session_state.ai_breakdowns[todoinput] = response.text
            
            st.rerun()

    def remove_task(task_name):
        if task_name in st.session_state.tasks:
            # Filter out the removed task while keeping everything else
            st.session_state.tasks = [task for task in st.session_state.tasks if task != task_name]
            st.session_state.dates = [date for i, date in enumerate(st.session_state.dates) if st.session_state.tasks[i] != task_name]
            st.session_state.ai_breakdowns = {task: breakdown for task, breakdown in st.session_state.ai_breakdowns.items() if task != task_name}

            st.rerun()

    # Iterate over tasks without using enumerate()
    for task in list(st.session_state.tasks):  # Using list() to avoid iteration issues during removal
        task_uuid = shortuuid.uuid()  # Generate a unique ID for the remove button
        
        col1, col2, col3 = st.columns([2, 1, 1])

        with col2:
            if st.button('Remove', key=f"remove_{task_uuid}"):
                remove_task(task)

        with col1:
            st.write(task)

        with col3:
            index = st.session_state.tasks.index(task)
            st.write(st.session_state.dates[index])

        # Display AI Breakdown for each task
        if task in st.session_state.ai_breakdowns:
            st.text_area(f'AI Task Breakdown for: {task}', st.session_state.ai_breakdowns[task], height=200)

elif page == 'AI Text Extraction':
    st.title('Image to Text')
    st.sidebar.write('This is an AI-powered tool that extracts text from an image (including handwritten text).')

    text = st.camera_input('Take a picture to scan:')

    if text:
        img = Image.open(text)

        responses = model.generate_content(contents=["What text is written in the image?", img])
        st.write(responses.text)
