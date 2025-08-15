# config.py
import os
import streamlit as st
from dotenv import load_dotenv

# Load .env locally
load_dotenv()

def get_secret(key: str) -> str:
    """
    Get a secret from Streamlit Cloud or local .env.
    """
    if key in st.secrets:  # running on Streamlit Cloud
        return st.secrets[key]
    return os.getenv(key)  # running locally

OPENAI_API_KEY = get_secret("OPENAI_API_KEY")
SERPER_API_KEY = get_secret("SERPER_API_KEY")
