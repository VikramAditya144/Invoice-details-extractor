import streamlit as st
import pytesseract
from pdf2image import convert_from_path
import openai
import os
from dotenv import load_dotenv
load_dotenv()

# Configure OpenAI API Key
openai.api_key = os.getenv('OPENAI_API_KEY')

# Streamlit App UI
st.title("Invoice Details Extractor")

# File uploader
uploaded_file = st.file_uploader("Upload an Invoice PDF", type=["pdf"])

# Process the PDF if uploaded
if uploaded_file is not None:
    with st.spinner('Processing...'):
        # Save the uploaded file to a temporary location
        with open("temp_invoice.pdf", "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Convert PDF to images
        pages = convert_from_path("temp_invoice.pdf")

        # Extract text using OCR
        invoice_text = ""
        for page in pages:
            invoice_text += pytesseract.image_to_string(page)

        # Use OpenAI to extract relevant details
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Extract the following details from this invoice:\n\n{invoice_text}\n\n"
                   "1. Customer details\n"
                   "2. Products\n"
                   "3. Total Amount",
            max_tokens=500
        )


        # Extracted details
        extracted_details = response.choices[0].text.strip()

        # Display extracted details
        st.subheader("Extracted Details")
        st.text(extracted_details)

        # Remove the temporary file
        os.remove("temp_invoice.pdf")
