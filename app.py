import streamlit as st
import traceback
import os
import fastparquet
import pandas as pd
from core.data_loader import Data

st.set_page_config(
    page_title="Lending Risk Analysis & Approval Prediction",
    page_icon="🏦",
    layout="wide",
)

# Step 1: Minimal session state init
if "data_loaded" not in st.session_state:
    st.session_state.data_loaded = False

# Step 2: Upload and convert only if not already done
if not st.session_state.data_loaded:
    st.subheader("📂 Upload Your Loan Data File")
    uploaded_file = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx"])

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

            st.success("✅ File successfully uploaded and saved as Parquet.")
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
