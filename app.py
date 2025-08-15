import streamlit as st
from dotenv import load_dotenv
from ui.dashboard import render
from config import OPENAI_API_KEY, SERPER_API_KEY


load_dotenv()
st.set_page_config(page_title="SCOUT — Founder Radar", layout="wide")
render()
