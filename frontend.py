# Step1: Setup UI with streamlit (model provider, model, system prompt, query)
import streamlit as st
import requests

st.set_page_config(page_title="LanGraph Agent UI", layout="wide")
st.title("AI Chatbot Agents")
st.write("Create and Interact with the AI Agents!")

system_prompt = st.text_area("Define your AI Agent:", height=70, placeholder="Type your system prompt here...")

MODEL_NAMES_GROQ = ["llama-3.3-70b-versatile", "llama3-70b-8192"]
MODEL_NAMES_OPENAI = ["gpt-4o-mini"]

provider = st.radio("Select Provider:", ("Groq", "OpenAI"))

if provider == "Groq":
    selected_model = st.selectbox("Select Groq Model:", MODEL_NAMES_GROQ)
elif provider == "OpenAI":
    selected_model = st.selectbox("Select OpenAI Model:", MODEL_NAMES_OPENAI)

allow_web_search = st.checkbox("Allow Web Search")

user_query = st.text_area("Enter your query:", height=70, placeholder="Ask Anything!")

API_URL = "http://127.0.0.1:9999/chat"

# Only run this when the button is clicked
if st.button("Ask Agent"):
    if user_query.strip():
        payload = {
            "model_name": selected_model,
            "model_provider": provider,
            "system_prompt": system_prompt,
            "messages": [user_query],
            "allow_search": allow_web_search
        }

        response = requests.post(API_URL, json=payload)

        if response.status_code == 200:
            response_data = response.json()

            if "error" in response_data:
                st.error(response_data["error"])
            else:
                st.subheader("Agent Response")
                final_response = response_data.get("response", "No response received.")
                st.markdown(f"**Final Response:** {final_response}")
        else:
            st.error(f"Request failed with status code {response.status_code}")
