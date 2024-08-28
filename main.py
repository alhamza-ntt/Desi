import streamlit as st
import time
import urllib.request
import json
def req(question):
    data = {"chat_input" : question}

    body = str.encode(json.dumps(data))
    #PROMOPTFLOW_CONFIG["api_key"]



    url = "https://desi-resturant.francecentral.inference.ml.azure.com/score"
    api_key = "vayqqVeISQ0T2Kwm21btoTTUIL3gGakH"
    if not api_key:
        raise Exception("A key should be provided to invoke the endpoint")
    headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}



    req = urllib.request.Request(url, body, headers)

    try:
        response = urllib.request.urlopen(req)

        result = response.read()
        return(json.loads(result)["chat_output"])
    except urllib.error.HTTPError as error:
        return("The request failed with status code: " + str(error.code))

        # return the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
        return(error.info())
        return(error.read().decode("utf8", 'ignore'))















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
