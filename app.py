import streamlit as st
from dotenv import load_dotenv
from ui.dashboard import render

load_dotenv()
st.set_page_config(page_title="SCOUT — Founder Radar", layout="wide")
render()
