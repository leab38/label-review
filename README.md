# Label Review Site

## Introduction
This site is intended to allow a user to upload a label picture and review it based on the [labeling requirements](https://www.ttb.gov/regulated-commodities/labeling/labeling-resources) set out by the The Alcohol and Tobacco Tax and Trade Bureau (TTB), a bureau of the Department of the Treasury. 

Label form: https://www.ttb.gov/system/files/images/pdfs/forms/f510031.pdf

### How to run it on your own machine (Windows)
1. Open command line
2. Go to Git project folder
3. .venv\Scripts\activate.bat
4. pip install -r requirements.txt
5. python -m streamlit run streamlit_app.py (this will open the project in your default web browser and run it locally)

### Using the app
There are two modes for ease of understanding how the app works. 
#### Mode 1: Upload Your Own Files
With mode 1, you select a product type ('wine','distilled spirits', or 'malt beverages'), input the label information into a web form, and upload front and back labels. When you press "Start Verification", this kicks off a PaddleOCR-driven text recognition program to review the uploaded labels and look for the information from your form, along with the language of the Government Warning.

#### Mode 2: Use Sample Data
If you don't have files or want to just run the app in the pre-tested context, there is a sample CSV file with data that matches with the sample label images. If you select this option, all you have to do is select a product type ('wine','distilled spirits', or 'malt beverages') and press 'Start Verification' to run the process on the sample data.

## Comments and Notes
This app is intended only as a proof of concept. Given more time to revise it could be iterated upon to create something even more impactful, but the goal was to demo what might be done.

The idea behind this is that the user could upload images and form data (not necessarily by hand) and then have this do a first comparison. The label reviewer could then use it as an initial review of their checklist. If something is clearly present, then that checklist item is considered complete and only those noted as missing would need to be validated.

### Future Implementation Ideas
1. Use pre-processing to improve optical character recognition results. Consider how to resolve the issue where words are joined together. (In "malt beverages" sample data, the "Brand Name" does appear in the image, but PaddleOCR recognizes it as ToTable instead of To Table.)
2. Improve error handling to make potential issues clearer.
3. Connect directly to form data, so that it is not manual entry. (I iniitally implemented the user input this way, but felt that creating a CSV with the relevant information would be laborious for a simple test.)
4. Include additional fields. In the instructions README (added as a file within this project), one of the users mentioned a long list of items to be verified, so this is just a short sample of what is being checked.
5. Additional checks on the government warning. This prototype only checks that the words "government warning" appear in all caps and the language of the warning is found verbatim within the same image. At the moment, the app does not verify that the text of GOVERNMENT WARNING is in bold text and it does not validate font sizes.
6. Identify further methods of reducing user input or intervention. While many parts of this process can be automated, it would need to be determined whether there are points at which a user needs to validate that the automation is doing what is expected of it, to not increase delays to request processing.