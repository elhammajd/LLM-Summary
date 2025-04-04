import streamlit as st
from llm_langchain_summary import main as llm_main

# Clear Streamlit cache (using legacy caching if available)
if hasattr(st, "runtime"):
    st.runtime.legacy_caching.clear_cache()

st.set_page_config(layout="wide")
st.title("Text Summarization ✍️")

st.sidebar.subheader("Summarization using GPT-3.5 & LangChain")
st.sidebar.write("Enter the details below:")

url = st.sidebar.text_input("Blog URL to summarize")
api_key = st.sidebar.text_input("Enter OpenAI API Key", type="password")

st.sidebar.write("----")
st.sidebar.subheader("About this App:")
st.sidebar.write("Designed by **Shubham Mandowara** to showcase text summarization using GPT-3.5 and LangChain.")
st.sidebar.write("----")
st.sidebar.subheader("Follow:")
st.sidebar.markdown(
    "[![Linkedin](https://img.icons8.com/material-outlined/48/000000/linkedin.png)](https://www.linkedin.com/in/shubhammandowara/) " +
    "[![Github](https://img.icons8.com/material-outlined/48/000000/github.png)](https://github.com/ShubhamMandowara)"
)

st.info("Hit Enter to get the summary once URL and API Key are provided.", icon="ℹ️")

VIDEO_DATA = 'https://youtu.be/8ae8JAfW4rY?si=BhCGmqiMAin7pwe5'
st.video(VIDEO_DATA)

if url and api_key:
    with st.spinner("Generating summary..."):
        try:
            summary = llm_main(url=url, open_api_key=api_key)
            st.write("**Summary:**")
            st.write(summary)
        except Exception as e:
            st.error(f"Error: {e}")
else:
    st.write("Please enter both the Blog URL and OpenAI API Key to proceed.")
