import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
import qrcode
from io import BytesIO
import json
import hashlib

st.set_page_config(page_title="AgriChain Analytics", layout="wide", initial_sidebar_state="expanded")

st.title("AgriChain Analytics")
st.markdown("Decentralized Supply Chain Traceability & AI Yield Anomaly Verification Engine")

# Helper: Generate QR Code Image
def generate_qr(data_str):
    qr = qrcode.QRCode(version=1, box_size=8, border=2)
    qr.add_data(data_str)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buf = BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()

# Helper: Simple AI Yield Validation using Isolation Forest
def verify_yield_anomaly(land_acres, weight_quintals):
    # Simulated historical distribution baseline (Normal range: 5 to 35 quintals per acre)
    np.random.seed(42)
    normal_acres = np.random.uniform(1, 10, 100)
    normal_yields = normal_acres * np.random.uniform(10, 25, 100)
    
    X_train = np.column_stack((normal_acres, normal_yields))
    
    model = IsolationForest(contamination=0.05, random_state=42)
    model.fit(X_train)
    
    X_input = np.array([[land_acres, weight_quintals]])
    prediction = model.predict(X_input) # 1 = Normal, -1 = Anomaly
    
    yield_ratio = weight_quintals / land_acres
    
    # Flag impossible yields (e.g. > 45 quintals per acre)
    if prediction[0] == -1 or yield_ratio > 45.0 or yield_ratio < 1.0:
        return False, yield_ratio
    return True, yield_ratio

# State Management
if 'ledger' not in st.session_state:
    st.session_state.ledger = []

tab1, tab2, tab3 = st.tabs(["Farmer Batch Logging", "Blockchain Ledger & QR", "Consumer Verification"])

with tab1:
    st.subheader("Farmer Harvest Logging Portal")
    col1, col2 = st.columns(2)
    
    with col1:
        farm_id = st.text_input("Farm ID", "FARM-HPU-01")
        region = st.selectbox("Region", ["Shimla", "Mandi", "Solan", "Kangra"])
        crop_type = st.selectbox("Organic Crop", ["Organic Wheat", "Organic Apple", "Organic Potato"])
    
    with col2:
        land_acres = st.number_input("Land Size (Acres)", min_value=0.5, value=2.0, step=0.5)
        harvest_quintals = st.number_input("Harvested Weight (Quintals)", min_value=1.0, value=30.0, step=5.0)

    if st.button("Submit Batch for AI Verification"):
        is_valid, ratio = verify_yield_anomaly(land_acres, harvest_quintals)
        
        batch_id = f"BATCH-{len(st.session_state.ledger) + 101}"
        
        if is_valid:
            # Generate cryptographic mock hashes
            payload = f"{batch_id}-{farm_id}-{region}-{crop_type}-{land_acres}-{harvest_quintals}"
            ipfs_hash = "Qm" + hashlib.sha256(payload.encode()).hexdigest()[:44]
            tx_hash = "0x" + hashlib.sha256((payload + "polygon").encode()).hexdigest()[:40]
            
            record = {
                "batch_id": batch_id,
                "farm_id": farm_id,
                "region": region,
                "crop": crop_type,
                "land_acres": land_acres,
                "harvest_quintals": harvest_quintals,
                "yield_per_acre": round(ratio, 2),
                "status": "Verified & Minted",
                "ipfs_hash": ipfs_hash,
                "polygon_tx": tx_hash
            }
            st.session_state.ledger.append(record)
            st.success(f"AI Audit Passed! Yield ratio: {round(ratio, 2)} Q/Acre. Batch minted on Polygon Ledger.")
            st.json(record)
        else:
            st.error(f"Fraud Warning: AI Audit Failed! Yield ratio ({round(ratio, 2)} Q/Acre) exceeds realistic crop bounds. Blocked from blockchain ledger.")

with tab2:
    st.subheader("Verified Batches & Dynamic QR Generation")
    if len(st.session_state.ledger) == 0:
        st.info("No verified batches present on the ledger. Log a batch in Tab 1.")
    else:
        for idx, item in enumerate(st.session_state.ledger):
            with st.expander(f"{item['batch_id']} - {item['crop']} ({item['region']})"):
                c1, c2 = st.columns([2, 1])
                with c1:
                    st.write(f"**Farm ID:** {item['farm_id']}")
                    st.write(f"**Land Size:** {item['land_acres']} Acres")
                    st.write(f"**Harvest Weight:** {item['harvest_quintals']} Quintals")
                    st.write(f"**IPFS Hash:** `{item['ipfs_hash']}`")
                    st.write(f"**Polygon TX:** `{item['polygon_tx']}`")
                with c2:
                    qr_payload = json.dumps({
                        "batch_id": item['batch_id'],
                        "farm_id": item['farm_id'],
                        "status": item['status'],
                        "ipfs": item['ipfs_hash']
                    })
                    qr_bytes = generate_qr(qr_payload)
                    st.image(qr_bytes, caption="Scan Package QR", width=150)

with tab3:
    st.subheader("Consumer Product Traceability Portal")
    search_batch = st.text_input("Enter Batch ID or Scan Payload", "BATCH-101")
    
    if st.button("Verify Provenance"):
        found = False
        for item in st.session_state.ledger:
            if item['batch_id'] == search_batch:
                found = True
                st.success("100% Authentic Organic Produce Verified")
                m1, m2, m3 = st.columns(3)
                m1.metric("Farm Region", item['region'])
                m2.metric("Land Area", f"{item['land_acres']} Acres")
                m3.metric("AI Yield Audit", f"{item['yield_per_acre']} Q/Acre (Normal)")
                st.write(f"**Cryptographic Proof:** `{item['polygon_tx']}`")
                break
        if not found:
            st.warning("Batch not found or failed organic yield verification checks.")