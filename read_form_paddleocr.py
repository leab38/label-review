# from argparse import ArgumentParser
import sys
import streamlit as st

from paddleocr import PaddleOCR
import pandas as pd
from sys import stderr

import text_fixing

sample_file = 'label images/sample_label_form.csv'

# product = 'wine'
# product = 'distilled spirits'
# product = 'malt beverages'

warning_statement = '''GOVERNMENT WARNING: (1) According to the Surgeon General, women
    should not drink alcoholic beverages during pregnancy because of the risk of
    birth defects. (2) Consumption of alcoholic beverages impairs your ability to 
    drive a car or operate machinery, and may cause health problems. '''

def build_requirements_dict(product,data):
    requirements_df = data[data['TYPE_OF_PRODUCT'].str.lower() == product.lower()].replace({pd.NA: ''})
    '''Requirements'''
    requirements_dict = {'BRAND_NAME':[requirements_df.iloc[0]['BRAND_NAME']]
                                ,'FANCIFUL_NAME':[requirements_df.iloc[0]['FANCIFUL_NAME']]
                                ,'NAME':[requirements_df.iloc[0]['NAME_AND_ADDRESS'].split('\n')[0]]
                                ,'ADDRESS':[requirements_df.iloc[0]['NAME_AND_ADDRESS'].split('\n')[1]]}

    
    if product.lower() == 'wine':
        requirements_dict['GRAPE_VARIETAL']=[requirements_df.iloc[0]['GRAPE_VARIETAL']]
        requirements_dict['WINE_APPELLATION']=[requirements_df.iloc[0]['WINE_APPELLATION']]

    else:
        print(f"Product type '{product}' not recognized.")
    print(requirements_dict)
    return requirements_dict

@st.cache_resource(show_spinner="Loading Paddle OCR")
def load_paddle():
    PaddleOCR(lang='en', use_angle_cls=True, ocr_version="PP-OCRv4")

def get_text_from_image(image_path):
    ocr = load_paddle()
    result = ocr.predict(image_path)
    text_dict = {}
    for item in result:
        text_dict.update(dict(zip(item.get('rec_texts', []), item.get('rec_scores', []))))
        full_text = text_fixing.reconstruct_text(item.get('rec_texts', []), 
                                                 item.get('rec_boxes', []))
    return text_dict, full_text


def main(mode,product,data):
    if mode == 'Use Sample Data':
        if product == 'distilled spirits':
            label_front_path = 'label images/Distilled_Spirits_TTB_Ex_Front.png'
            label_back_path = 'label images/Distilled_Spirits_TTB_Ex_Back.png'
        elif product == 'wine':
            label_front_path = 'label images/Wine_TTB_Ex_Front.png'
            label_back_path = 'label images/Wine_TTB_Ex_Back.png'

    requirements_dict = build_requirements_dict(product,data)
    print('--- Label Front Text RESULT START ---')
    front_text,full_front_text = get_text_from_image(label_front_path)
    print(front_text)
    front_lower = {k.lower():v for k,v in front_text.items()}
    print('--- Label Front Text RESULT END ---')

    print('--- Label Back Text RESULT START ---')
    back_text,full_back_text = get_text_from_image(label_back_path)
    print(full_back_text)
    back_lower = {k.lower():v for k,v in back_text.items()}
    print('--- Label Back Text RESULT END ---')

    for key,value in requirements_dict.items():
        print(f"{key}: {requirements_dict[key]}")
        if value[0].lower() in front_lower.keys():
            print(f"{key} found in front text with confidence {front_lower[value[0].lower()]}.")
            requirements_dict[key].append(f"{key} ({value[0]}) found in front text with confidence {front_lower[value[0].lower()]}.")
        elif value[0].lower() in back_lower.keys():
            print(f"{key} found in back text with confidence {back_lower[value[0].lower()]}.")
            requirements_dict[key].append(f"{key} ({value[0]}) found in back text with confidence {back_lower[value[0].lower()]}.")
        else:
            print(f"{key} not found in either front or back text.")
            requirements_dict[key].append(f"{key} ({value[0]}) not found in either front or back text.")

    if 'GOVERNMENT WARNING:' in full_front_text:
        print("GOVERNMENT WARNING found in front text.")
        score = text_fixing.is_paragraph_in_image(warning_statement, full_front_text)
        print(f"Fuzzy match score for front text: {score[1]}. Meets threshold: {score[0]}.")
        requirements_dict['GOVERNMENT WARNING'] = ['GOVERNMENT WARNING',f"GOVERNMENT WARNING found in front text with fuzzy match score {score[1]}. Meets threshold: {score[0]}."]
    elif 'GOVERNMENT WARNING:' in full_back_text:
        print("GOVERNMENT WARNING found in back text.")
        score = text_fixing.is_paragraph_in_image(warning_statement, full_back_text)
        print(f"Fuzzy match score for back text: {score[1]}. Meets threshold: {score[0]}.")
        requirements_dict['GOVERNMENT WARNING'] = ['GOVERNMENT WARNING',f"GOVERNMENT WARNING found in back text with fuzzy match score {score[1]}. Meets threshold: {score[0]}."]
    else:
        print("GOVERNMENT WARNING not found in either front or back text.")
        requirements_dict['GOVERNMENT WARNING'] = ['GOVERNMENT WARNING',"GOVERNMENT WARNING not found in either front or back text."]

    return requirements_dict

if __name__ == "__main__":
    try:
        main(mode=st.session_state.mode,product=st.session_state.product,data=pd.read_csv(sample_file))
    except KeyboardInterrupt as k:
        stderr.write("ok, bye\n")
        exit(1)
    except Exception as e:
        stderr.write(f"Error: {e}")
        exit(1)