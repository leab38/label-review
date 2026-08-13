# Label Review Site

## Introduction
This site is intended to allow a user to upload a label picture and review it based on the [labeling requirements](https://www.ttb.gov/regulated-commodities/labeling/labeling-resources) set out by the The Alcohol and Tobacco Tax and Trade Bureau (TTB), a bureau of the Department of the Treasury. 

Label form: https://www.ttb.gov/system/files/images/pdfs/forms/f510031.pdf

### How to run it on your own machine (Windows)
1. Open command line
2. Go to Git project folder
3. .venv\Scripts\activate.bat
4. pip install -r requirements.txt
5. python -m streamlit run streamlit_app.py

## Comments and Notes
This app is intended only as a proof of concept. Given more time to revise it could be iterated upon to create something even more impactful, but the goal was to demo what might be done.

The idea behind this is that the user could upload images and form data (not necessarily by hand) and then have this do a first comparison. The label reviewer could then use it as an initial review of their checklist. If something is clearly present, then that checklist item is considered complete and only those noted as missing would need to be validated.

### Future Implementation Ideas
1. Use pre-processing to improve optical character recognition results. Consider how to resolve the issue where words are joined together. (In "malt beverages" sample data, the "Brand Name" does appear in the image, but PaddleOCR recognizes it as ToTable instead of To Table.)
2. Improve error handling to make potential issues clearer.
3. Connect to form data, so that it is not manual entry. (I iniitally implemented the user input this way, but felt that creating a CSV with the relevant information would be laborious for a simple test.)
