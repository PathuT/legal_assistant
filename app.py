import os
import streamlit as st
import google.generativeai as genai

# Set up the Gemini API configuration
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Create the model with the desired configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Instantiate the generative model
model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config=generation_config,
    system_instruction=(
        "You are an expert in criminal laws and your role is to assist junior counsels "
        "and law students. Your task is to engage in conversations about criminal law, answer legal "
        "questions, and provide real-time information on case law based on user input queries. Ensure "
        "that your explanations are clear and precise, using legal terminology in a way that is understandable "
        "for your audience. Provide accurate, fast, and user-friendly responses using the Gemini API. Aim to "
        "help users strengthen their legal knowledge by offering relevant case law examples and practical applications. "
        "Strictly no response for non-criminal law topics."
    ),
)

# Start a chat session
chat_session = model.start_chat(history=[])

# Streamlit app layout
st.set_page_config(page_title="Criminal Law Assistant", layout="wide")
st.title("Criminal Law Assistant")
st.write("Ask questions related to criminal law and receive detailed responses with case examples.")

# Initialize session state for storing chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display chat history
for msg in st.session_state["messages"]:
    if msg["user"]:
        st.markdown(f"**User:** {msg['text']}")
    else:
        st.markdown(f"**Assistant:** {msg['text']}")

# Input field for user questions
user_input = st.text_input("Enter your question:", key="input")

# Generate a response when the user submits a question
if st.button("Send"):
    if user_input:
        # Append user input to the chat history
        st.session_state["messages"].append({"user": True, "text": user_input})
        
        with st.spinner("Generating response..."):
            response = chat_session.send_message(user_input)
        
        # Append model response to the chat history
        st.session_state["messages"].append({"user": False, "text": response.text})
        st.experimental_rerun()  # Refresh the UI to show new messages
