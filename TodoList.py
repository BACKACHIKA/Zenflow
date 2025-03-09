import streamlit as st
import google.generativeai as genai
import shortuuid
from PIL import Image


genai.configure(api_key="AIzaSyBEnO9-HQgK4dVACYvYmJCJ58L_kh4lJ1I")
model = genai.GenerativeModel("gemini-1.5-flash")



tab1, tab2= st.tabs(['AI Powered To Do list','Handwriting Text Extraction'])


with tab1:
    st.title('To Do List')
    st.write(
        'This is a to-do list app that uses AI to break down your tasks into simple, manageable sub-tasks.')

    if 'tasks' not in st.session_state:
        st.session_state.tasks = []
    if 'dates' not in st.session_state:
        st.session_state.dates = []

    col1, col2 = st.columns(2)

    with col1:
        todoinput = st.text_input('Enter a task:')

    with col2:
        date = st.date_input('Enter the deadline')

    if st.button('Add Task'):
        if todoinput and todoinput not in st.session_state.tasks:
            st.session_state.tasks.append(todoinput)
            st.session_state.dates.append(date)
            st.rerun()


    def remove_task(task_name,dates):
            
            st.session_state.tasks.pop(task_name)
            st.session_state.dates.pop(dates)
            st.rerun()



    for task in range(len(st.session_state.tasks)):


        col1, col2, col3 = st.columns([2, 1, 1])

        with col2:
            if st.button('Remove', key='Remove'+str(task)):
                remove_task(task,task)

        with col1:
            st.write(st.session_state.tasks[task])
            st.write(st.session_state.dates[task])




        response = model.generate_content(
            f'Break down the following task: {st.session_state.tasks[task]} into chunks that can be completed in. sessions. '
            'Split it into stages, so Stage 1: Do this, Stage 2: Do this, and so on for 10 stages. '
            'Each stage must have max. 20 words. Keep it all the same font. Add a new line before every stage. '
            'However if a task is given,you must break it down.Like you need to.Even if its a repeat task,you need to.No matter what break down the task.'
        )
        st.text_area(f'AI Task Breakdown for: {st.session_state.tasks[task]}', response.text, height=200)

with tab2:
    st.title('Image to Text')
    st.write('This is an AI-powered tool that extracts text from an image (including handwritten text).')

    text = st.camera_input('Take a picture to scan:')

    if text:
        img = Image.open(text)

        responses = model.generate_content(contents=["What text is written in the image?", img])
        st.write(responses.text)




