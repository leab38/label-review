import streamlit as st
import pandas as pd
from io import StringIO
from paddleocr import PaddleOCR
from PIL import Image

import read_form_paddleocr
sample_file = 'label images/sample_label_form.csv'

st.title("Label Review")
st.write("Upload your label and label form and start the verification process.")

# st.write("st.session_state object:", st.session_state)
st.session_state.verification = False
st.session_state.requirements_dict = {}

mode = st.radio("Select Mode", ("Upload Files", "Use Sample Data"),key="mode")

options = ["wine", "distilled spirits", "malt beverages"]
product = st.selectbox("Select Product Type", options,key="product")

#default images
if product == 'distilled spirits':
    label_front_path = 'label images/Distilled_Spirits_TTB_Ex_Front.png'
    label_back_path = 'label images/Distilled_Spirits_TTB_Ex_Back.png'
elif product == 'wine':
    label_front_path = 'label images/Wine_TTB_Ex_Front.png'
    label_back_path = 'label images/Wine_TTB_Ex_Back.png'
elif product == 'malt beverages':
    label_front_path = 'label images/Malt_TTB_Ex_Front.png'
    label_back_path = 'label images/Malt_TTB_Ex_Back.png'

#file upload

if mode == "Upload Files":
    with st.form("label information"):
        st.write("Label Information")
        brand_name = st.text_input('Brand Name')
        fanciful = st.text_input('Fanciful Name')
        company_name = st.text_input('Name')
        address = st.text_input('Address')
        if product.lower() == 'wine':
            varietal = st.text_input('Grape Varietal')
            appellation = st.text_input('Wine Appellation')
        submit = st.form_submit_button('Save Label Information')

    if product.lower() == 'wine':
        st.session_state.requirements_dict= {'BRAND NAME':[brand_name],'FANCIFUL NAME': [fanciful],'NAME':[company_name],'ADDRESS':[address],'GRAPE_VARIETAL':[varietal],'WINE_APPELLATION':[appellation]}
    else:
        st.session_state.requirements_dict= {'BRAND NAME':[brand_name],'FANCIFUL NAME': [fanciful],'NAME':[company_name],'ADDRESS':[address]}
        
    label_front = st.file_uploader("Upload Label Front", type=["png", "jpg", "jpeg", "webp"])
    if label_front is not None:
        st.write("Label Front Uploaded")
        front_image = Image.open(label_front)
        label_front_path = read_form_paddleocr.convert_uploaded_image(label_front)

    label_back = st.file_uploader("Upload Label Back", type=["png", "jpg", "jpeg", "webp"])
    if label_back is not None:
        st.write("Label Back Uploaded")
        back_image = Image.open(label_back)
        label_back_path = read_form_paddleocr.convert_uploaded_image(label_back)

if mode == 'Use Sample Data':
    # Display the data in a table
    data = pd.read_csv(sample_file)
    st.write("Uploaded Data:")
    st.dataframe(data[data['TYPE_OF_PRODUCT'].str.lower() == product.lower()].replace({pd.NA: ''}))
    st.session_state.requirements_dict = read_form_paddleocr.build_requirements_dict(product,data)
    front_image = Image.open(label_front_path)
    back_image = Image.open(label_back_path)

# Add a button to start the verification process
if st.button("Start Verification"):
    st.write("Verification process started...")

    st.session_state.front_image = label_front_path
    st.session_state.back_image = label_back_path

    col1, col2 = st.columns(2)
    with col1:
        st.image(front_image, caption="Label Front")
    with col2:
        st.image(back_image, caption="Label Back")

    verification_dict = read_form_paddleocr.main(st.session_state.mode,st.session_state.product,st.session_state.requirements_dict, label_front_path, label_back_path)
    st.session_state.verification = True

    st.write("Verification Results:")
    for key, value in verification_dict.items():
        st.write(value[-1])

if st.session_state.verification == True:
    print(verification_dict)