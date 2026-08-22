import streamlit as st
import qrcode
from io import BytesIO
import json
import time
from ml_engine import YieldAnomalyDetector

# Page configuration
st.set_page_config(
    page_title="AgriChain Analytics",
    page_icon="🌾",
    layout="wide"
)

# Initialize Session State to store verified batches locally
if "batches" not in st.session_state:
    st.session_state.batches = []

# Title & Header
st.title("AgriChain Analytics")
st.caption("Decentralized Traceability & AI Anomaly Verification Engine for Organic Produce")
st.markdown("---")

# Initialize ML Engine
detector = YieldAnomalyDetector()

# Tabs for different user roles
tab1, tab2, tab3 = st.tabs(["Farmer Batch Logging", "Blockchain Ledger & QR", "Consumer Verification"])

# ---------------------------------------------------------
# TAB 1: FARMER BATCH LOGGING
# ---------------------------------------------------------
with tab1:
    st.header("Log New Organic Harvest Batch")
    
    col1, col2 = st.columns(2)
    
    with col1:
        farmer_id = st.text_input("Farmer ID / Aadhaar Hash", "FRM-2026-8842")
        crop_type = st.selectbox("Crop Type", ["Organic Wheat", "Organic Rice", "Organic Pulses", "Organic Cotton", "Organic Vegetables"])
        land_area = st.number_input("Land Area (in Acres)", min_value=0.1, value=2.0, step=0.5)
        
    with col2:
        harvest_weight = st.number_input("Harvested Weight (in Quintals)", min_value=0.1, value=30.0, step=5.0)
        location = st.text_input("Farm Geo-Coordinates", "28.9931° N, 77.0151° E (Sonipat, HR)")
        certification_no = st.text_input("Organic Certificate Ref No.", "ORG-IN-2026-9041")

    if st.button("Submit Batch for AI Verification", type="primary"):
        with st.spinner("Running ML Anomaly Detection Model..."):
            time.sleep(0.5)
            # Call ML engine
            result = detector.verify_yield(land_area_acres=land_area, harvest_weight_quintals=harvest_weight)

        if result["status"] == "PASS":
            st.success(f"AI Yield Audit Passed! Yield Ratio: {result['yield_ratio']} q/acre.")
            
            # Simulate Blockchain & IPFS commit
            batch_id = len(st.session_state.batches) + 1
            ipfs_hash = f"QmXyZ{hash(farmer_id + str(time.time())) % 1000000000000000}"
            tx_hash = f"0x{hash(str(batch_id) + ipfs_hash) & 0xffffffffffffffffffffffffffffffff:032x}"
            
            batch_data = {
                "batch_id": batch_id,
                "farmer_id": farmer_id,
                "crop_type": crop_type,
                "land_area": land_area,
                "harvest_weight": harvest_weight,
                "yield_ratio": result["yield_ratio"],
                "location": location,
                "ipfs_hash": ipfs_hash,
                "tx_hash": tx_hash,
                "status": "VERIFIED_ON_CHAIN"
            }
            
            st.session_state.batches.append(batch_data)
            st.info(f"🔗 Batch #{batch_id} successfully minted on Polygon Testnet! IPFS Hash: `{ipfs_hash}`")
            
        else:
            st.error(f"🚨 AI Yield Audit FLAGGED! {result['reason']}")
            st.warning("Batch flagged for manual inspection. Cannot be minted to blockchain ledger.")

# ---------------------------------------------------------
# TAB 2: BLOCKCHAIN LEDGER & QR GENERATOR
# ---------------------------------------------------------
with tab2:
    st.header("Verified Batches & Dynamic QR Generator")
    
    if not st.session_state.batches:
        st.info("No batches logged yet. Use Tab 1 to submit a harvest batch.")
    else:
        for b in st.session_state.batches:
            with st.expander(f"Batch #{b['batch_id']} - {b['crop_type']} ({b['status']})"):
                c1, c2 = st.columns([2, 1])
                
                with c1:
                    st.write(f"**Farmer ID:** {b['farmer_id']}")
                    st.write(f"**Geo-Coordinates:** {b['location']}")
                    st.write(f"**Yield Ratio:** {b['yield_ratio']} q/acre ({b['harvest_weight']} q / {b['land_area']} acres)")
                    st.write(f"**IPFS Certificate Hash:** `{b['ipfs_hash']}`")
                    st.write(f"**Polygon Tx Hash:** `{b['tx_hash']}`")
                
                with c2:
                    # Generate QR Code
                    qr_data = json.dumps({
                        "batch_id": b["batch_id"],
                        "crop": b["crop_type"],
                        "farmer": b["farmer_id"],
                        "ipfs": b["ipfs_hash"],
                        "tx": b["tx_hash"]
                    })
                    
                    qr = qrcode.QRCode(version=1, box_size=5, border=2)
                    qr.add_data(qr_data)
                    qr.make(fit=True)
                    img = qr.make_image(fill_color="black", back_color="white")
                    
                    buf = BytesIO()
                    img.save(buf, format="PNG")
                    byte_im = buf.getvalue()
                    
                    st.image(byte_im, caption=f"Package QR Code (Batch #{b['batch_id']})", width=180)

# ---------------------------------------------------------
# TAB 3: CONSUMER VERIFICATION
# ---------------------------------------------------------
with tab3:
    st.header("Consumer Trust Verification Portal")
    st.write("Simulate scanning product package QR code to verify 100% genuine organic origin.")
    
    if not st.session_state.batches:
        st.warning("Log at least one batch in Tab 1 to test consumer verification.")
    else:
        selected_batch_id = st.selectbox("Select Batch ID to Scan", [b["batch_id"] for b in st.session_state.batches])
        target_batch = next((b for b in st.session_state.batches if b["batch_id"] == selected_batch_id), None)
        
        if target_batch:
            st.markdown("### Verified Supply Chain Origin")
            st.success("Authenticated Organic Product")
            
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Batch ID", f"#{target_batch['batch_id']}")
            m2.metric("Crop", target_batch["crop_type"])
            m3.metric("AI Yield Status", "PASSED")
            m4.metric("Blockchain Ledger", "VERIFIED")
            
            st.markdown("#### Supply Chain Provenance Trail")
            st.json({
                "Origin Farm Coordinates": target_batch["location"],
                "Organic Certification IPFS Hash": target_batch["ipfs_hash"],
                "Polygon Smart Contract Transaction": target_batch["tx_hash"],
                "AI Yield Ratio Check": f"{target_batch['yield_ratio']} Quintals/Acre (Normal Range)",
                "Verification Timestamp": "2026-08-22 UTC"
            })