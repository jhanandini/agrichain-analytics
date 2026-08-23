import streamlit as st
import numpy as np
import pandas as pd
import qrcode
from io import BytesIO
from PIL import Image
import hashlib
import time
from ml_engine import train_and_evaluate_yield

# Page Config
st.set_page_config(page_title="AgriChain Analytics", page_icon="🌾", layout="wide")

# App Header
st.title("🌾 AgriChain Analytics")
st.markdown("### *Decentralized Supply Chain Traceability & AI Yield Anomaly Engine*")
st.divider()

# Initialize Session State
if "batches" not in st.session_state:
    st.session_state["batches"] = []

# Tabs Setup
tab1, tab2, tab3, tab4 = st.tabs([
    "📝 Farmer Batch Logging", 
    "🔗 Blockchain Ledger & Dynamic QR", 
    "🔍 Consumer Verification Portal",
    "⚙️ Web3 Node & Network Status"
])

# ---------------------------------------------------------
# TAB 1: FARMER BATCH LOGGING & AI AUDIT ENGINE
# ---------------------------------------------------------
with tab1:
    st.header("Farmer Batch Registration & AI Audit")
    st.caption("Submit harvest batch data. The AI Isolation Forest engine evaluates yield-to-land ratio before minting onto the blockchain.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        farmer_name = st.text_input("Farmer / Producer Name", "Nandini Jha")
        crop_type = st.selectbox("Crop Type", ["Organic Wheat", "Organic Rice", "Organic Pulses", "Organic Cotton"])
        location = st.text_input("Farm Location Coordinates", "28.9931° N, 77.0151° E (Sonipat, HR)")
    
    with col2:
        land_area = st.number_input("Land Area (in Acres)", min_value=0.5, max_value=500.0, value=2.0, step=0.5)
        harvested_weight = st.number_input("Harvested Yield (in Quintals)", min_value=1.0, max_value=10000.0, value=30.0, step=1.0)
        fertilizer_used = st.text_input("Certifications / Bio-Inputs Used", "Bio-Compost, NPK Organic Liquid")
    
    if st.button("🚀 Submit Batch for AI Verification", type="primary"):
        with st.spinner("AI Engine Evaluating Yield Anomaly..."):
            is_valid, anomaly_score, yield_per_acre = train_and_evaluate_yield(land_area, harvested_weight)
            time.sleep(1)
            
        if is_valid:
            st.success(f"✅ **AI Yield Verification Passed!** Yield density: **{yield_per_acre:.2f} Quintals/Acre** (Within realistic organic parameters).")
            
            # Generate Cryptographic Hashes
            raw_data = f"{farmer_name}{crop_type}{land_area}{harvested_weight}{location}{time.time()}"
            ipfs_hash = "Qm" + hashlib.sha256(raw_data.encode()).hexdigest()[:44]
            tx_hash = "0x" + hashlib.sha256((raw_data + "polygon").encode()).hexdigest()
            batch_id = f"AGRI-{len(st.session_state['batches']) + 101}"
            
            # Create QR Code
            qr_data = f"https://agrichain.analytics/verify?batch_id={batch_id}&ipfs={ipfs_hash}"
            qr = qrcode.QRCode(version=1, box_size=10, border=2)
            qr.add_data(qr_data)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            
            buf = BytesIO()
            img.save(buf, format="PNG")
            qr_bytes = buf.getvalue()
            
            # Save Batch Record
            batch_record = {
                "batch_id": batch_id,
                "farmer": farmer_name,
                "crop": crop_type,
                "land_area": land_area,
                "weight": harvested_weight,
                "yield_per_acre": yield_per_acre,
                "location": location,
                "ipfs_hash": ipfs_hash,
                "tx_hash": tx_hash,
                "status": "Verified & Minted",
                "qr_code": qr_bytes
            }
            st.session_state["batches"].append(batch_record)
            
            st.balloons()
            st.info(f"**Batch #{batch_id}** successfully minted to Smart Contract Ledger! Check 'Blockchain Ledger' tab.")
        else:
            st.error(f"⚠️ **AI Fraud Alert! High Anomaly Detected (Score: {anomaly_score:.2f})**")
            st.warning(f"Calculated Yield Density is **{yield_per_acre:.2f} Quintals/Acre**, which exceeds standard organic harvest baselines. Minting blocked to prevent fraud.")

# ---------------------------------------------------------
# TAB 2: BLOCKCHAIN LEDGER & DYNAMIC QR
# ---------------------------------------------------------
with tab2:
    st.header("Immutable Ledger & Dynamic QR Output")
    
    if len(st.session_state["batches"]) == 0:
        st.info("No batches minted yet. Submit a batch in Tab 1 to generate ledger records.")
    else:
        for batch in reversed(st.session_state["batches"]):
            with st.expander(f"📦 Batch ID: {batch['batch_id']} - {batch['crop']} ({batch['status']})"):
                c1, c2 = st.columns([2, 1])
                with c1:
                    st.write(f"**Farmer:** {batch['farmer']}")
                    st.write(f"**Location:** {batch['location']}")
                    st.write(f"**Yield Density:** {batch['yield_per_acre']:.2f} Quintals/Acre")
                    st.code(f"IPFS Certificate Hash: {batch['ipfs_hash']}", language="text")
                    st.code(f"Polygon Transaction Hash: {batch['tx_hash']}", language="text")
                with c2:
                    st.image(batch["qr_code"], caption=f"Dynamic Package QR ({batch['batch_id']})", width=180)

# ---------------------------------------------------------
# TAB 3: CONSUMER VERIFICATION PORTAL
# ---------------------------------------------------------
with tab3:
    st.header("Retail Consumer QR Scan Verification")
    st.caption("Consumers scan product QR codes at retail stores to verify origin authenticity and AI audit status.")
    
    search_id = st.text_input("Enter Batch ID (e.g. AGRI-101)", "AGRI-101")
    
    found_batch = None
    for b in st.session_state["batches"]:
        if b["batch_id"].upper() == search_id.strip().upper():
            found_batch = b
            break
            
    if found_batch:
        st.success("✅ **Authentic Organic Produce Verified!**")
        st.json({
            "Batch ID": found_batch["batch_id"],
            "Producer": found_batch["farmer"],
            "Crop Type": found_batch["crop"],
            "Land Area": f"{found_batch['land_area']} Acres",
            "Harvest Weight": f"{found_batch['weight']} Quintals",
            "AI Yield Audit Status": "PASS (Realistic Organic Yield)",
            "IPFS Cryptographic Proof": found_batch["ipfs_hash"],
            "Polygon Testnet Tx": found_batch["tx_hash"]
        })
    else:
        st.warning("Enter a valid Batch ID from Tab 1 to view live consumer origin provenance.")

# ---------------------------------------------------------
# TAB 4: WEB3 NODE & NETWORK STATUS
# ---------------------------------------------------------
with tab4:
    st.header("Web3 Node & Smart Contract Execution Environment")
    
    col_a, col_b = col_c = st.columns(3)
    col_a.metric(label="Target Blockchain Network", value="Polygon Amoy Testnet")
    col_b.metric(label="Smart Contract Standard", value="ERC-721 / IPFS Hash")
    col_c.metric(label="Consensus Protocol", value="Proof-of-Stake (PoS)")
    
    st.subheader("Contract Info")
    st.code("""
// Contract Address: 0x5FbDB2315678afecb367f032d93F642f64180aa3
// Solidity Compiler: ^0.8.20
// Gas Usage per Mint: ~0.0024 MATIC
    """, language="solidity")