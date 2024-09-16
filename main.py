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

    # Initialize session state for storing conversation history
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # React to user input
    if user_input := st.chat_input("Write your message"):
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(user_input)

        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            response = get_assistant_response(user_input, st.session_state.messages)
            message_placeholder.markdown(response)

        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})


if __name__ == "__main__":
    main()
