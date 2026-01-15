import streamlit as st
import requests
import uuid

st.set_page_config(layout="wide")

st.title("RAG-Retrieval Augmented Generation")

st.write("Welcome to the RAG-Retrieval Augmented Generation app.")

if "session_id" not in st.session_state:
    st.session_state.session_id = None

if "token" not in st.session_state:
    st.session_state.token = None

with st.sidebar:
    st.sidebar.header("Login/Logout")
    username = st.sidebar.text_input("Username", value="")
    password = st.sidebar.text_input("Password", type="password", value="")

    if st.button("Login"):
        if username and password:
            # In a real app, you would verify username and password here
            #st.session_state.token = get_token(username, password)
            st.success(f"Logged in as {username}")
            st.session_state.session_id = str(uuid.uuid4())
            st.write(f"Session ID: {st.session_state.session_id}")
        else:
            st.warning("Please enter username and password to login.")
    if st.button("Logout"):
        if username and password:
            st.session_state.session_id = None
            st.session_state.token = None
            st.success("Logged out")
        else:
            st.warning("Please enter username and password to login.")



system_prompt="You are a helpful assistant "

#Can you suggest me 10 projects names that I can build using LLMs
user_prompt=st.text_area("User Prompt", value="", height=100)


if st.button("Run"):
    # call API to evaluate the platform based on the selected criteria
    url = "http://localhost:8000/ask"
    payload = {
        "system_prompt": system_prompt,
        "user_prompt": user_prompt
    }

    headers={"Content-Type": "application/json", "Accept": "application/json"}
             
    st.write(payload)

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        result = response.json()
        st.write(result['answer'])
        # st.write(result['sources'])

    st.success("Process completed!")