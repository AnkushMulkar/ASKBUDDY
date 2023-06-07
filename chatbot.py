# Author: Ankush Mulkar (https://ankushmulkar.github.io/Portfolio/)

# Importing the required libraries
import streamlit as st
from streamlit_chat import message
from streamlit_extras.colored_header import colored_header
from streamlit_extras.add_vertical_space import add_vertical_space
from hugchat import hugchat
from PIL import Image, ImageDraw, ImageOps

# Page Configuration
# Application title and body
st.set_page_config(page_title="ASK BUDDY", page_icon="", layout='wide')

# Title of application
st.title("ASK BUDDY")
#st.markdown("### By [Ankush Mulkar](https://ankushmulkar.github.io/Portfolio/)")

# Page Structure
with st.sidebar:
    st.title("ASK BUDDY")
    st.markdown('''
        ### 
    By [Ankush Mulkar](https://ankushmulkar.github.io/Portfolio/)
    ''')

# Session State
if 'generated' not in st.session_state:
    st.session_state['generated'] = ["Hi, I'm Ankush. How can I assist you today?"]
if 'past' not in st.session_state:
    st.session_state['past'] = ['Hello!']

# Application layout
input_container = st.container()
colored_header(label='', description='', color_name='blue-30')
response_container = st.container()

# User inputs
def get_text():
    input_text = st.text_input("Text here to ask me...", "", key="input")
    return input_text

# Applying the user input box
with input_container:
    user_input = get_text()

# Function to crop image in circular shape
def crop_to_circle(image):
    width, height = image.size
    mask = Image.new("L", (width, height), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, width, height), fill=255)
    result = ImageOps.fit(image, mask.size, centering=(0.5, 0.5))
    result.putalpha(mask)
    return result

# Loading and cropping the user's profile image
profile_image = Image.open("ANKUSH.jpg")
profile_image = crop_to_circle(profile_image)

# Displaying the cropped profile image
st.sidebar.image(profile_image, use_column_width=True)

# Displaying the name below the profile image
st.sidebar.markdown("### Ankush Mulkar")

# Bot outputs
def generate_response(prompt):
    chatbot = hugchat.ChatBot(cookie_path="cookies.json")
    response = chatbot.chat(prompt)
    return response

# Conditional display of AI generated responses as a function of user provided prompts
with response_container:
    if user_input:
        response = generate_response(user_input)
        st.session_state.past.append(user_input)
        st.session_state.generated.append(response)
        
    if st.session_state['generated']:
        for i in range(len(st.session_state['generated'])):
            st.write("💬 User:", st.session_state['past'][i])
            st.write("💡 Ankush:", st.session_state['generated'][i])
