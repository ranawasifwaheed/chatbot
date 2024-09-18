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
    "You are a helpful and engaging assistant. Provide clear, friendly, and informative responses to a wide range "
    "of questions. Your goal is to assist users with their inquiries, whether they are about general knowledge, "
    "specific topics, or practical advice. If you don't have an answer, kindly suggest that they look for additional information."
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
        return f"Oops! Something went wrong: {e}"


def main():
    st.set_page_config(page_title="Knowledgeable Chatbot", page_icon=":speech_balloon:", layout="wide")

    # Custom CSS for hiding Streamlit branding and improving responsiveness
    st.markdown("""
    <style>
        /* Hide Streamlit branding and footer */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}

        /* Remove any default margin or padding */
        .stApp {
            margin: 0;
            padding: 0;
        }

        /* Chat message bubbles */
        .message-bubble {
            display: inline-block;
            padding: 8px;
            margin: 4px 0;
            border-radius: 8px;
            max-width: 85%;
            word-wrap: break-word;
        }
        .user {
            background-color: #d4edda; /* Light green */
            text-align: right;
            margin-left: auto;
        }
        .assistant {
            background-color: #fff3cd; /* Light yellow */
            text-align: left;
            margin-right: auto;
        }

        /* Responsive adjustments for chat bubbles */
        @media (max-width: 768px) {
            .message-bubble {
                max-width: 90%;
                font-size: 14px;
            }
        }

        @media (max-width: 480px) {
            .message-bubble {
                font-size: 12px;
                padding: 6px;
            }
        }

        @media (max-width: 375px) {
            .message-bubble {
                font-size: 11px;
                padding: 4px;
            }
        }

        @media (max-width: 320px) {
            .message-bubble {
                font-size: 10px;
                padding: 3px;
            }
        }

        /* Ensure minimal space above chat messages */
        .stTitle {
            margin-top: 0;
        }

        /* Custom CSS for chat input box */
        .stChatInput {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            padding: 8px;
            box-sizing: border-box;
            background-color: #fff;
            display: flex;
            align-items: center;
            border-top: 1px solid #ddd;
            z-index: 1000;
        }

        /* Custom CSS for the input field */
        .stChatInput textarea {
            flex: 1;
            padding: 8px;
            border-radius: 8px;
            border: 1px solid #ccc;
            font-size: 14px;
            box-sizing: border-box;
            resize: none;
            overflow: hidden;
            max-height: 100px; /* Limit height */
        }

        /* Custom CSS for the send button */
        .stChatInput button {
            border: none;
            background: #007bff;
            color: white;
            border-radius: 8px;
            padding: 6px 12px;
            cursor: pointer;
            font-size: 14px;
            box-sizing: border-box;
            margin-left: 8px;
            min-width: 80px;
        }
        .stChatInput button:focus {
            outline: none;
        }

        /* Ensure responsive behavior of input and button */
        @media (max-width: 768px) {
            .stChatInput textarea {
                font-size: 13px;
            }
            .stChatInput button {
                font-size: 13px;
                padding: 5px 10px;
            }
        }

        @media (max-width: 480px) {
            .stChatInput textarea {
                font-size: 12px;
            }
            .stChatInput button {
                font-size: 12px;
                padding: 4px 8px;
            }
        }

        @media (max-width: 375px) {
            .stChatInput textarea {
                font-size: 11px;
            }
            .stChatInput button {
                font-size: 11px;
                padding: 3px 6px;
            }
        }

        @media (max-width: 320px) {
            .stChatInput textarea {
                font-size: 10px;
            }
            .stChatInput button {
                font-size: 10px;
                padding: 2px 4px;
            }
        }
    </style>
    """, unsafe_allow_html=True)

    st.title("Knowledgeable Chatbot")

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
