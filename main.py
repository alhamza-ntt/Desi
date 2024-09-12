import streamlit as st
import time
import urllib.request
import json
def req(q):
    url = "https://desi-fkfec2dxbqh8ffdu.eastus-01.azurewebsites.net/ask"
    # Create the payload with the question
    payload = {
        "question": q
    }

    # Send the POST request with the JSON payload
    response = requests.post(url, json=payload)

    # Print the response from the server
    if response.status_code == 200:
        return (response.json()["response"])
    else:
        return (f"Failed to send request. Status code: {response.status_code}")















# Streamed response emulator
def response_generator(question):
    response = req(question)
    lines = response.splitlines()  # Split by lines to preserve formatting
    for line in lines:
        words = line.split()  # Split each line into words
        for word in words:
            yield word + " "  # Stream word by word
            time.sleep(0.05)
        yield "\n"  # Add a newline after each line



st.title("Simple chat UI For DeSi")



# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        response = st.write_stream(response_generator(prompt))
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
