import streamlit as st
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

# Access environment variables
api_key = os.getenv("OPEN_AI_KEY")
model = os.getenv("MODEL_NAME")

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

# Define system prompt to guide the assistant
system_prompt = (
    "You are an educational assistant. Provide informative and accurate responses to questions "
    "about various subjects such as science, history, math, literature, and more. If you don't "
    "know the answer, politely suggest the user search for more information."
)


def get_assistant_response(user_input, messages):
    """
    Generates a response using OpenAI's API.
    :param user_input: User input for the chatbot.
    :param messages: List of message history.
    :return: Generated response as a string.
    """
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "system", "content": system_prompt}] + messages + [
                {"role": "user", "content": user_input}],
        )
        response_message = response.choices[0].message.content
        return response_message

    except Exception as e:
        return f"Exception occurred: {e}"


def main():
    st.set_page_config(page_title="Educational Chatbot", page_icon=":speech_balloon:", layout="wide")

    # Custom CSS for removing Streamlit branding and responsive design
    st.markdown("""
    <style>
        /* Hide Streamlit branding and footer */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}

        /* Chat message bubbles */
        .message-bubble {
            display: inline-block;
            padding: 10px;
            margin: 5px 0;
            border-radius: 10px;
            max-width: 80%;
        }
        .user {
            background-color: #d1e7dd;
            text-align: right;
        }
        .assistant {
            background-color: #f8d7da;
            text-align: left;
        }

        /* Responsive adjustments */
        @media (max-width: 768px) {
            .message-bubble {
                max-width: 90%; /* Adjust max width for mobile devices */
                font-size: 16px; /* Slightly larger text for readability */
            }
        }

        /* Further adjustments for smaller screens */
        @media (max-width: 480px) {
            .message-bubble {
                font-size: 14px; /* Slightly smaller text for smaller screens */
            }
        }

        /* Adjust padding and margins for smaller screens */
        body {
            padding: 0;
            margin: 0;
        }

    </style>
    """, unsafe_allow_html=True)

    st.title("Educational Chatbot")

    # Initialize session state for storing conversation history
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f'<div class="message-bubble user">{message["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="message-bubble assistant">{message["content"]}</div>', unsafe_allow_html=True)

    # React to user input
    if user_input := st.chat_input("Write your message"):
        # Add user message to session state and display it
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.markdown(f'<div class="message-bubble user">{user_input}</div>', unsafe_allow_html=True)

        # Generate assistant's response
        response = get_assistant_response(user_input, st.session_state.messages)
        st.session_state.messages.append({"role": "assistant", "content": response})

        # Display assistant's response
        st.markdown(f'<div class="message-bubble assistant">{response}</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()
