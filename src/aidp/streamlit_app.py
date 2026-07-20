import streamlit as st
import requests
import json
import time

st.set_page_config(page_title="AIDP Platform", page_icon="🔬", layout="wide")

st.title("🔬 Artificial Intelligence Discovery Platform (AIDP)")
st.subheader("Hackathon Edition: Powered by Gemma, Supabase, and Render")

st.markdown("""
Welcome to the Streamlit visualization hub. This interface is tightly integrated with our backend orchestrator 
to dynamically visualize the reasoning chains of our 20+ prominent agents.
""")

col1, col2 = st.columns([1, 2])

with col1:
    st.header("Launch Discovery")
    query = st.text_area("Scientific Query", "Alpha-Synuclein Peptide Inhibitor")
    
    if st.button("Run Pipeline (Gemma Backend)"):
        with st.spinner("Initializing Master Orchestrator..."):
            try:
                # Assuming backend is deployed on Render or running locally
                response = requests.post("http://localhost:8000/api/discovery", json={"query": query})
                if response.status_code == 200:
                    job_id = response.json().get("job_id")
                    st.success(f"Pipeline started! Job ID: {job_id}")
                    
                    # Polling
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    for i in range(100):
                        time.sleep(0.5)
                        status_res = requests.get(f"http://localhost:8000/api/discovery/{job_id}").json()
                        if status_res.get("status") == "completed":
                            progress_bar.progress(100)
                            status_text.text("Execution Complete!")
                            st.session_state["result"] = status_res.get("result")
                            break
                        progress_bar.progress((i + 1) % 100)
                        status_text.text("Agents debating and verifying constraints...")
            except Exception as e:
                st.error(f"Backend offline: {e}")

with col2:
    st.header("Orchestration Results")
    if "result" in st.session_state:
        st.json(st.session_state["result"])
    else:
        st.info("Awaiting pipeline execution...")

st.divider()
st.caption("Backend powered by FastAPI, Firebase Auth, and Supabase Epistemic Ledger. Deployed via Render.")
