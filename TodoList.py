import streamlit as st
import google.generativeai as genai
import shortuuid

column1, column2, column3 = st.columns(3)

st.sidebar.title('Choose a tool:')
page = st.sidebar.selectbox('Go to', ('To Do List', 'AI Text Extraction'))

if page == 'To Do List':
    st.title('To Do list:')
    st.sidebar.write('This is a to-do list app that uses AI to break down your tasks into simple,manageable sub-tasks.) ')

    if 'key' not in st.session_state:
        st.session_state.key = []

    column1, column2, column3 = st.columns(3)

    with column2:
        todoinput = st.text_input('Firstly,enter a task:')
        date = st.date_input('Enter the deadline')

    with column3:
        st.write('\n')
        st.write('\n')
        add = st.button('Add', icon=":material/add:")

    if 'tasks' not in st.session_state:
        st.session_state.tasks = []

    if 'dates' not in st.session_state:
        st.session_state.dates = []

    if 'add_clicked' not in st.session_state:
        st.session_state.add_clicked = False

    if add and not st.session_state.add_clicked:
        st.session_state.add_clicked = True
        st.session_state.tasks.append(todoinput)
        st.session_state.dates.append(date)
        todoinput = ""
        st.rerun()

    st.session_state.add_clicked = False #reset the add clicked state.

    def remove_task(task, date):
        st.session_state.tasks.remove(task)
        st.session_state.dates.remove(date)
        st.rerun()

    task_display = st.empty()
    with task_display.container():
        for i, task in enumerate(st.session_state.tasks):
            col1, col2, col3 = st.columns([2, 1, 1])

            with col2:
                st.button('Remove', key=str(shortuuid.uuid()),
                          on_click=lambda t=task, d=st.session_state.dates[i]: remove_task(t, d))

            with col1:
                st.write(task)

            with col3:
                st.write(st.session_state.dates[i])

            genai.configure(api_key="AIzaSyBEnO9-HQgK4dVACYvYmJCJ58L_kh4lJ1I")
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(
                'Break down the following task: ' + task +
                ' into chunks that can be completed in pomodoro sessions. Split it into stages, so Stage 1: Do this, Stage 2: Do this, and so on for 10 stages. Each stage must have max. 20 words. Keep it all the same font. Add a new line before every stage.Give the format as such that there is a new line after every stage.If no task is given,say Please enter a task above.')

            st.text_area('AI Task Breakdown', response.text)

elif page == 'AI Text Extraction':
    st.title('Image to text:')
    st.sidebar.write('This is an AI-powered tool that can extract text from an image(including handwritten text).')
    import streamlit as st
    from PIL import Image
    import google.generativeai as genai

    text = st.camera_input('Take a picture to scan:')

    if text:
        img = Image.open(text)

        genai.configure(api_key='AIzaSyBEnO9-HQgK4dVACYvYmJCJ58L_kh4lJ1I')
        model = genai.GenerativeModel("gemini-1.5-flash")

        responses = model.generate_content(contents=["What text is written in the image?", img])
        st.write(responses.text)
