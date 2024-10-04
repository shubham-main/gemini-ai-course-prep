import os
from email.policy import default

from PIL import Image

import streamlit as st
from streamlit import markdown
from streamlit_option_menu import option_menu

from gemini_utility import (load_gemini_pro_model,
                            gemini_pro_vision_response,
                            embedding_model_response,
                            gemini_pro_response)


# get the working directory
working_directory = os.path.dirname(os.path.abspath(__file__))

# setting up the page comfiguration
st.set_page_config(
    page_title="Shubham AI",
    page_icon="🧠",
    layout="centered"
)

with st.sidebar:

    selected = option_menu(menu_title= "Shubham AI",
                           options=["ChatBot",
                                    "Image Captioning",
                                    "Embed text",
                                    "Ask me Anything"],
                           menu_icon='robot', icons=['chat-dots-fill', 'image-fill',
                                                     'textarea-t', 'patch-question-fill'],
                           default_index=0)


# function to translate role between gemini-pro and streamlit terminology
def translate_role_for_streamlit(user_role):
    if user_role == 'model':
        return "assistant"
    else:
        return user_role


if selected == "ChatBot":

    model = load_gemini_pro_model()

    # Initialize chat session in streamlit if not already present
    if "chat_session" not in st.session_state:
        st.session_state.chat_session = model.start_chat(history=[])

    # streamlit page title
    st.title("🤖 ChatBot")

    # display the chat history
    for message in st.session_state.chat_session.history:
        with st.chat_message(translate_role_for_streamlit(message.role)):
            st.markdown(message.parts[0].text)

    # input field for user's message
    user_prompt = st.chat_input("Ask Shubham-AI...")

    if user_prompt:
        st.chat_message("user").markdown(user_prompt)

        gemini_response =st.session_state.chat_session.send_message(user_prompt)

        # display gemini-pro response
        with st.chat_message("assistant"):
            st.markdown(gemini_response.text)



# image captioning  Page
if selected == "Image Captioning":

    # streamlit page title
    st.title("📷 Snap Narrate")

    uploaded_image = st.file_uploader("Upload an image...", type=["jpg", "jpeg", "png"])

    if st.button("Generate Caption"):

        image = Image.open(uploaded_image)

        col1, col2 = st.columns(2)

        with col1:
            resized_image = image.resize((800,500))
            st.image(resized_image)

        default_prompt = "Write a short caption for this image"

        # getting respomse from gemini-pro-vision-model
        caption = gemini_pro_vision_response(default_prompt, image)

        with col2:
            st.info(caption)



# text embedding page
if selected == "Embed text":

    st.title("🔡 Embed Text")

    # input text box
    input_text = st.text_area(label="",placeholder="Enter the text to get the embeddings")

    if st.button("Get Embeddings"):
        response = embedding_model_response(input_text)
        st.markdown(response)

# question answering page
if selected == "Ask me Anything":

    st.title("? Ask me a question")

    # text box to enter prompt
    user_prompt = st.text_area(label="",placeholder="Ask Shubham-AI...")

    if st.button("Give me answer"):
        response = gemini_pro_response(user_prompt)
        st.markdown(response)