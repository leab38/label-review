import streamlit as st
import pandas as pd
from io import StringIO

# import read_form_paddleocr
sample_file = 'label images/sample_label_form.csv'

st.title("Label Review")
st.write("Upload your label and label form and start the verification process.")

st.write("st.session_state object:", st.session_state)
st.session_state.verification = False

mode = st.radio("Select Mode", ("Use Sample Data","Upload Files"),key="mode")

options = ["wine", "distilled spirits", "malt beverages"]
product = st.selectbox("Select Product Type", options,key="product")