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

#default images
if product == 'distilled spirits':
    label_front_path = 'label images/Distilled_Spirits_TTB_Ex_Front.png'
    label_back_path = 'label images/Distilled_Spirits_TTB_Ex_Back.png'
elif product == 'wine':
    label_front_path = 'label images/Wine_TTB_Ex_Front.png'
    label_back_path = 'label images/Wine_TTB_Ex_Back.png'

#file upload

if mode == "Upload Files":
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    if uploaded_file is not None:
        # Read the uploaded CSV file
        data = pd.read_csv(uploaded_file)

        # Display the data in a table
        st.write("Uploaded Data:")
        st.dataframe(data)

    label_front = st.file_uploader("Upload Label Front", type="png")
    if label_front is not None:
        st.write("Label Front Uploaded")

    label_back = st.file_uploader("Upload Label Back", type="png")
    if label_back is not None:
        st.write("Label Back Uploaded")

if mode == 'Use Sample Data':
    data = pd.read_csv(sample_file)

# Add a button to start the verification process
if st.button("Start Verification"):
    st.write("Verification process started...")

    col1, col2 = st.columns(2)
    with col1:
        st.image(label_front_path, caption="Label Front")
    with col2:
        st.image(label_back_path, caption="Label Back")

    requirements_dict = read_form_paddleocr.main(mode,product,data)
    st.session_state.verification = True

    st.write("Verification Results:")
    for key, value in requirements_dict.items():
        st.write(value[-1])

if st.session_state.verification == True:
    print(requirements_dict)