# AgriChain Analytics

Decentralized Supply Chain Traceability & AI Yield Anomaly Verification Engine for Organic Produce.

## Problem Statement
Over 40% of produce labeled as "Organic" in retail markets suffers from mislabeling or fraud, shortchanging both smallholder farmers and health-conscious consumers. Traditional paper certification systems are costly, slow, and prone to middleman tampering.

## Solution Overview
AgriChain Analytics combines Machine Learning Anomaly Detection with Blockchain Immutability to verify organic crop yield validity before minting batches onto a decentralized ledger.

1. Farmer Batch Logging: Farmers record yield details (Land Area vs. Harvested Weight).
2. AI Yield Audit Engine: An IsolationForest ML model validates if the land-to-yield ratio is realistic, blocking exaggerated submissions.
3. Smart Contract Ledger: Verified batches generate cryptographic IPFS hashes stored on Polygon smart contracts.
4. Dynamic QR Code Generation: Dynamic package QR codes allow consumers to scan and trace origin, geo-location, and verified audit trails instantly.

## Tech Stack
- Frontend & UI: Python, Streamlit
- Machine Learning: Scikit-Learn, NumPy, Pandas
- Blockchain: Solidity, Web3, Polygon, IPFS Storage
- Utilities: Python QRcode library

## How to Run Locally

1. Clone Repository:
git clone https://github.com/jhanandini/agrichain-analytics.git
cd agrichain-analytics

2. Install Dependencies:
pip install -r requirements.txt

3. Launch App:
streamlit run app.py
