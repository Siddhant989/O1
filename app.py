import streamlit as st
import traceback
import os
import fastparquet
import pandas as pd
from core.data_loader import Data
from PIL import Image

st.set_page_config(
    page_title="Mortage Analytics Tool",
    page_icon="🏦",
    layout="wide",
)
import html

    
# Path to logo image
# logo_path = os.path.join("assets", "static/logo.png")
# print(f"Logo path exists: {os.path.exists(logo_path)}")

# Create three columns: left (logo), center (header), right (spacer)
col1, col2, col3 = st.columns([1.5, 16, 2])

with col1:
    st.image("static/Sigmoid_logo_2x.png")
  

with col2:
    st.markdown("<h1 style='text-align: center;'>🏦 Sigmoid-Mortgage Analytics Tool</h1>", unsafe_allow_html=True)


with col3:
    # Dropdown-style contact bubble
    st.markdown("""
    <style>
    .dropdown {
        position: relative;
        display: inline-block;
        margin-top: 10px;
        float: right;
    }

    .dropdown-button {
        background-color: #E9F5FE;
        color: #0A2540;
        padding: 10px 16px;
        font-size: 14px;
        border: none;
        cursor: pointer;
        border-radius: 18px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }

    .dropdown-content {
        display: none;
        position: absolute;
        right: 0;
        background-color: #F9FAFB;
        min-width: 180px;
        padding: 10px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        z-index: 1;
    }

    .dropdown:hover .dropdown-content {
        display: block;
    }

    .dropdown-content a {
        color: #0A2540;
        text-decoration: none;
        display: block;
        font-size: 14px;
        margin-top: 5px;
    }
    </style>

    <div class="dropdown">
      <button class="dropdown-button">📞 Contact Us</button>
      <div class="dropdown-content">
        <b>Ravi Bajagur</b><br>
        <a href="tel:8959896843">8959896843</a>
      </div>
    </div>
    """, unsafe_allow_html=True)



# Step 1: Minimal session state init
if "data_loaded" not in st.session_state:
    st.session_state.data_loaded = False

if not st.session_state.data_loaded:
    st.markdown("""
    <style>
    .intro-text {
        font-size: 23px;
        font-weight: 600;
        color: #1e88e5;
        line-height: 1.7;
        background-color: #f5f7fa;
        border-radius: 16px;
        padding: 30px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
        margin-top: 20px;
    }
    </style>
""", unsafe_allow_html=True)


    st.markdown("""
        <div class="intro-text">
            Welcome to the Mortgage Analytics Tool – The Mortgage Analytics Tool is a powerful, intelligent assistant 
                designed to revolutionize the way lenders analyze and manage loan origination data. 
                Built with advanced data science and automation, this platform simplifies complex mortgage workflows, 
                enabling financial institutions to make faster, more accurate, and data-driven decisions. 
                From assessing borrower credibility to identifying risk patterns and generating real-time insights, 
                this tool streamlines the entire analytics process in an intuitive, conversational interface.
            <br><br>
            Whether you're a risk analyst, underwriter, or data strategist, the tool empowers you to upload datasets, 
                ask natural language questions, and receive instant, actionable responses. 
                No need to write SQL or dig through spreadsheets — just focus on insights that drive smarter lending decisions.
            <br><br>
            Built for flexibility and speed, the Mortgage Analytics Tool adapts to your data, supports regulatory needs, 
                and enhances transparency in the mortgage lifecycle. Discover a new standard in origination analytics.
        </div>


    """, unsafe_allow_html=True)

css = '''
<style>
    [data-testid='stFileUploader'] {
        width: max-content;
    }
    [data-testid='stFileUploader'] section {
        padding: 0;
        float: left;
    }
    [data-testid='stFileUploader'] section > input + div {
        display: none;
    }
    [data-testid='stFileUploader'] section + div {
        float: right;
        padding-top: 0;
    }

</style>
'''

st.markdown(css, unsafe_allow_html=True)

# Step 2: Upload and convert only if not already done
if not st.session_state.data_loaded:
    uploaded_file = st.file_uploader("Upload a CSV or Excel file",
        type=["csv", "xlsx"])

    if uploaded_file:
        try:
            # Load the data
            if uploaded_file.name.endswith(".csv"):
                df = pd.read_csv(uploaded_file, low_memory=False)
            elif uploaded_file.name.endswith(".xlsx"):
                df = pd.read_excel(uploaded_file)
            else:
                st.error("Only CSV and Excel files are supported.")
                st.stop()

            # Save to Parquet
            data_folder = os.path.join(os.getcwd(), "data")
            os.makedirs(data_folder, exist_ok=True)
            parquet_path = os.path.join(data_folder, "Origination.parquet")
            fastparquet.write(parquet_path, df, compression="snappy", write_index=False)

            st.success("✅ File successfully uploaded.")
            st.session_state.data = Data()
            st.session_state.data_loaded = True
            st.rerun()# Set page configuration

            # Optional: rerun to trigger interface cleanly

        except Exception as e:
            st.error(f"❌ Error processing file: {e}")
            st.stop()

# Step 3: Load Chat Interface after file is uploaded
if st.session_state.data_loaded:
    try:
        from chat_page import show_agentic_chat_interface
        show_agentic_chat_interface()
    except Exception as e:
        print(f"Error in chat interface: {e}")
        traceback.print_exc()
        st.error(
            "⚠️ Oops! Something went wrong. Please try your request again. If the issue continues, try refreshing or clearing the chat to reset things."
        )
