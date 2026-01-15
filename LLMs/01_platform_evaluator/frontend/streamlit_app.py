import streamlit as st
import requests
import uuid

st.set_page_config(layout="wide")

st.title("Platform Evaluator")

st.write("Welcome to the Platform Evaluator app. This application helps you evaluate different platforms based on various criteria.")

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



system_prompt=st.text_area("System Prompt", value="You are a helpful assistant that evaluates platforms based on user-defined criteria.", disabled=True)

#Can you suggest me 10 projects names that I can build using LLMs
user_prompt=st.text_area("User Prompt", value="", height=100)

model = st.selectbox("Model", ["gpt-4o-mini", "gpt-4o", "gpt-4o-2024-08-06", "gpt-4o-2024-08-06-preview", "gpt-4o-2024-08-06-preview-2"])

#mutiple selection box for evaluation criteria
# evaluation_criteria = st.multiselect("Select Evaluation Criteria", [
#     "Coherence of response", "Token limits and usage","Latency and response time","Scalability","Cost efficiency","Integration capabilities","User experience","Support and documentation","Security features","Customization options"])

if st.button("Evaluate Platform"):
    st.write("Evaluating platform with the following prompts:")
    st.write("**System Prompt:**", system_prompt)
    st.write("**User Prompt:**", user_prompt)
    # Here you would typically call your evaluation function or API

    # call API to evaluate the platform based on the selected criteria
    url = "http://localhost:8000/run_evaluation"
    payload = {
        "system_prompt": system_prompt,
        "user_prompt": user_prompt,
        "model": model
    }

    st.write("Sending evaluation request to the backend...")
    st.write(payload)

    headers={"Content-Type": "application/json", "Accept": "application/json"}
             
    #Pending activity - "authorization": "Bearer YOUR_API_KEY_HERE"}

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        result = response.json()
        st.write("**Evaluation Results:**")
        st.write("**Response Text:**")
        st.write(result['response'])
        st.write("**Latency:**")
        st.write(result['latency'])
        st.write("**Total Tokens Used:**")
        st.write(result['total_tokens'])

    st.success("Platform evaluation completed!")