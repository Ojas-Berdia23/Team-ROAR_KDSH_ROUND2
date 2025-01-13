import numpy as np
import streamlit as st
import PyPDF2  
from preprocess import predict

st.set_page_config(
    page_title="Research Paper Analyzer",
    page_icon="📃",
    layout="wide",
)

st.markdown("""
    <style>
        .title {
            color: #E1E1E1FF;
            font-size: 36px;
            font-weight: bold;
            text-align: center; /* This centers the text */
        }

        .publishable{
            font-size: 30px;
            color: #01BB0EFF;
            text-align: center; /* This centers the text */
        }

        .nonpublishable{
            font-size: 30px;
            color: #CC1111FF;
            text-align: center; /* This centers the text */
        }

        /* Style for headers with background color */
        .header {
            background-color: #2c2f38;  /* Darker background */
            color: white;  /* White text color */
            padding: 10px;
            border-radius: 5px;
        }
    </style>
""", unsafe_allow_html=True)

# Apply the styles to elements
st.markdown('<div class="title">Test Your Research Paper</div>', unsafe_allow_html=True)

paper = st.file_uploader("Choose a Paper to upload", type="pdf")

if paper is not None:
    # Show a spinner while waiting for the prediction
    with st.spinner('Analyzing the research paper...'):
        # Read the PDF file
        reader = PyPDF2.PdfReader(paper)
        text = ""

        # Extract text from all pages
        for page in reader.pages:
            text += page.extract_text()

        # Make prediction
        prediction = predict(text)
    
    # Clear the file uploader after prediction
    st.session_state.uploaded_file = None
    
    # Display result based on the prediction
    if prediction[0] == 0:
        st.markdown('<div class="nonpublishable">This Research Paper is Non-Publishable</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="publishable">This Research Paper is Publishable</div>', unsafe_allow_html=True)
        st.markdown('<div class="header">Suggested Conference:</div>', unsafe_allow_html=True)
        st.write(prediction[1].upper())
    
    st.markdown('<div class="header">Reason:</div>', unsafe_allow_html=True)
    st.write(prediction[2])
