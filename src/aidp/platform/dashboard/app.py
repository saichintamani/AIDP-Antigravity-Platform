import pandas as pd  # type: ignore
import requests
import streamlit as st

# Assume the FastAPI server is running locally on 8000
API_URL = "http://localhost:8000"

st.set_page_config(page_title="AIDP Laboratory Dashboard", layout="wide")

st.title("🔬 AIDP Laboratory Dashboard")
st.markdown("Monitor the Autonomous Scientific Laboratory in real-time.")

# Fetch Metrics
try:
    metrics_res = requests.get(f"{API_URL}/metrics")
    if metrics_res.status_code == 200:
        metrics = metrics_res.json()

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Spend (USD)", f"${metrics['total_spend_usd']:,.2f}")
        col2.metric("Tokens Consumed", f"{metrics['total_tokens_consumed']:,}")
        col3.metric("Research Throughput", metrics["research_throughput"])
        col4.metric("Novel Discoveries", metrics["novel_discoveries"])
except Exception:
    st.error("Could not connect to AIDP API Gateway.")

st.divider()

st.subheader("Intelligent Scheduler Queue")
try:
    queue_res = requests.get(f"{API_URL}/scheduler/queue")
    if queue_res.status_code == 200:
        queue_data = queue_res.json()
        if queue_data:
            df = pd.DataFrame(queue_data)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("Queue is currently empty.")
except Exception:
    st.error("Failed to fetch queue.")

st.divider()

st.subheader("Launch Research Campaign")
with st.form("campaign_form"):
    domain = st.selectbox(
        "Scientific Domain", ["Oncology", "Virology", "Materials Science", "Genomics"]
    )
    goal = st.text_area(
        "Research Goal", "e.g., Identify a novel allosteric inhibitor for KRAS G12C."
    )
    submitted = st.form_submit_button("Launch Campaign")

    if submitted:
        try:
            res = requests.post(f"{API_URL}/campaigns", json={"goal": goal, "domain": domain})
            if res.status_code == 200:
                st.success(f"Campaign launched successfully! ID: {res.json().get('campaign_id')}")
            else:
                st.error("Failed to launch campaign.")
        except Exception as e:
            st.error(f"Error launching campaign: {e}")
