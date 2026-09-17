import streamlit as st
import pandas as pd
from pipeline import validate_farm_batch
from analytics import detect_yield_anomalies

st.set_page_config(page_title="AgriChain Analytics", layout="wide")

st.title("AgriChain Analytics")
st.markdown("Farm-to-Consumer Organic Produce Traceability and Anomaly Verification Engine")

# Manual Batch Log Form
st.sidebar.header("Log Harvest Batch")
farm_id = st.sidebar.text_input("Farm ID", "FARM-101")
region = st.sidebar.selectbox("Region", ["Shimla", "Mandi", "Solan", "Kangra"])
commodity = st.sidebar.selectbox("Crop", ["Organic Apple", "Organic Potato", "Organic Tomato"])
land_size = st.sidebar.number_input("Land Size (Acres)", min_value=0.1, value=2.0)
harvest_weight = st.sidebar.number_input("Harvest Weight (KG)", min_value=1.0, value=2500.0)

if 'batch_data' not in st.session_state:
    st.session_state.batch_data = pd.DataFrame(columns=[
        'farm_id', 'region', 'commodity', 'land_size_acres', 'harvest_weight_kg'
    ])

if st.sidebar.button("Verify and Submit Batch"):
    new_entry = pd.DataFrame([{
        'farm_id': farm_id,
        'region': region,
        'commodity': commodity,
        'land_size_acres': land_size,
        'harvest_weight_kg': harvest_weight
    }])
    st.session_state.batch_data = pd.concat([st.session_state.batch_data, new_entry], ignore_index=True)

if not st.session_state.batch_data.empty:
    validated_df = validate_farm_batch(st.session_state.batch_data)
    processed_df = detect_yield_anomalies(validated_df)
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Batches Logged", len(processed_df))
    col2.metric("Valid Organic Batches", len(processed_df[~processed_df['is_fraudulent_yield']]))
    col3.metric("Flagged Fraudulent Batches", len(processed_df[processed_df['is_fraudulent_yield']]))
    
    st.divider()
    st.subheader("Batch Verification Records")
    st.dataframe(processed_df, use_container_width=True)
else:
    st.info("Log a batch using the sidebar to run the verification engine.")