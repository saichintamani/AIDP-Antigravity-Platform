import glob
import os
from pathlib import Path

import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="AIDP Phase R2: Human Pilot",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --- Theme Toggle ---
if "theme" not in st.session_state:
    st.session_state.theme = "dark"

def toggle_theme():
    st.session_state.theme = "light" if st.session_state.theme == "dark" else "dark"

IS_DARK = st.session_state.theme == "dark"

# --- Premium CSS ---
css_vars = f"""
:root {{
    --bg: {'#09090b' if IS_DARK else '#ffffff'};
    --bg-subtle: {'#0c0c0f' if IS_DARK else '#f9fafb'};
    --card: {'#0c0c0f' if IS_DARK else '#ffffff'};
    --card-hover: {'#131316' if IS_DARK else '#f4f4f5'};
    --border: {'#1e1e24' if IS_DARK else '#e4e4e7'};
    --border-subtle: {'#16161a' if IS_DARK else '#f0f0f2'};
    --text: {'#fafafa' if IS_DARK else '#09090b'};
    --text-muted: #71717a;
    --text-dim: {'#52525b' if IS_DARK else '#a1a1aa'};
    --accent: #2563eb;
    --accent-muted: #1d4ed8;
    --green: {'#22c55e' if IS_DARK else '#16a34a'};
    --green-muted: {'rgba(34,197,94,0.12)' if IS_DARK else 'rgba(22,163,74,0.08)'};
    --red: {'#ef4444' if IS_DARK else '#dc2626'};
    --red-muted: {'rgba(239,68,68,0.12)' if IS_DARK else 'rgba(220,38,38,0.08)'};
    --amber: {'#f59e0b' if IS_DARK else '#d97706'};
    --amber-muted: {'rgba(245,158,11,0.12)' if IS_DARK else 'rgba(217,119,6,0.08)'};
    --shadow: {'none' if IS_DARK else '0 1px 3px rgba(0,0,0,0.04), 0 1px 2px rgba(0,0,0,0.03)'};
    --radius: 10px;
}}
"""

global_css = """
<style>
header[data-testid="stHeader"], #MainMenu, footer, [data-testid="stToolbar"],
[data-testid="stDecoration"], [data-testid="stStatusWidget"], .stDeployButton,
div[data-testid="stSidebarCollapsedControl"] {
    display: none !important;
}
html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"], .main, .block-container, section[data-testid="stMain"] {
    background-color: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'DM Sans', -apple-system, sans-serif !important;
}
.block-container {
    padding: 2rem 2.5rem 3rem !important;
    max-width: 1360px !important;
}
.brand {
    font-size: 1.5rem;
    font-weight: 700;
    letter-spacing: -0.05em;
    color: var(--text);
    margin-bottom: 2rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.metric-card { background: var(--card); border: 1px solid var(--border); border-radius: var(--radius); padding: 1.25rem 1.4rem; box-shadow: var(--shadow); margin-bottom: 1rem; }
.metric-label { font-size: 0.78rem; color: var(--text-muted); font-weight: 500; text-transform: uppercase; letter-spacing: 0.05em; }
.metric-value { font-size: 1.45rem; font-weight: 700; color: var(--text); letter-spacing: -0.02em; margin-top: 0.5rem; }
.badge { display: inline-block; padding: 3px 10px; border-radius: 6px; font-size: 0.72rem; font-weight: 600; text-transform: uppercase; }
.badge-red { color: var(--red); background: var(--red-muted); border: 1px solid rgba(239,68,68,0.2); }
.badge-green { color: var(--green); background: var(--green-muted); border: 1px solid rgba(34,197,94,0.2); }
.badge-blue { color: var(--accent); background: rgba(37,99,235,0.15); border: 1px solid rgba(37,99,235,0.3); }

/* Markdown specific overrides */
.stMarkdown p { color: var(--text) !important; font-size: 1.05rem; line-height: 1.6; }
.stMarkdown h1 { color: var(--text) !important; font-weight: 700; font-size: 2rem; }
.stMarkdown h2 { color: var(--text) !important; font-weight: 600; margin-top: 2rem; border-bottom: 1px solid var(--border-subtle); padding-bottom: 0.5rem; }
.stMarkdown h3 { color: var(--text) !important; font-weight: 600; color: var(--accent); }
.stMarkdown blockquote {
    border-left: 4px solid var(--accent);
    background: var(--bg-subtle);
    padding: 1rem 1.5rem;
    border-radius: 0 8px 8px 0;
    color: var(--text-dim) !important;
    font-style: italic;
}
</style>
"""

st.markdown(f"<style>{css_vars}</style>", unsafe_allow_html=True)
st.markdown(global_css, unsafe_allow_html=True)


def get_surveys():
    search_path = os.path.join("data", "human_pilot_surveys", "*.md")
    files = glob.glob(search_path)
    return sorted(files)

def parse_survey(filepath):
    with open(filepath, encoding='utf-8') as f:
        content = f.read()
    
    # Split into sections roughly
    parts = content.split("## 2. Candidate Experiments to Rank")
    evidence_part = parts[0] if len(parts) > 0 else ""
    experiments_part = "## 2. Candidate Experiments to Rank\n" + parts[1] if len(parts) > 1 else ""
    
    # Extract Case ID
    case_id = "Unknown"
    for line in evidence_part.splitlines():
        if line.startswith("**Case ID:**"):
            case_id = line.replace("**Case ID:**", "").strip()
            break
            
    return case_id, evidence_part, experiments_part

# --- Layout ---
head_left, head_right = st.columns([8, 1])
with head_left:
    st.markdown("""
    <div class="brand">
        🧬 AIDP Phase R2: Human Expert Evaluation Portal
    </div>
    """, unsafe_allow_html=True)
with head_right:
    theme_label = "☀️ Light" if IS_DARK else "🌙 Dark"
    st.button(theme_label, on_click=toggle_theme, use_container_width=True)


# --- Tabs ---
tab1, tab2 = st.tabs(["📝 Phase R2: Human Expert Evaluation", "📊 Phase R3: Scaled Generative Discovery"])

with tab1:
    surveys = get_surveys()
    if not surveys:
        st.error("No survey files found in data/human_pilot_surveys/")
    else:
        # Sidebar / Case Selection
        st.sidebar.markdown("### 📋 Cases (Phase R2)")
        selected_file = st.sidebar.radio("Select Case to Evaluate", surveys, format_func=lambda x: Path(x).stem.replace("survey_", ""))
        
        case_id, evidence, experiments = parse_survey(selected_file)
        
        # Display stats in cards
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Case ID</div>
                <div class="metric-value">{case_id}</div>
            </div>
            """, unsafe_allow_html=True)
        with c2:
            st.markdown("""
            <div class="metric-card">
                <div class="metric-label">Status</div>
                <div class="metric-value"><span class="badge badge-blue">Pending Review</span></div>
            </div>
            """, unsafe_allow_html=True)
        with c3:
            st.markdown("""
            <div class="metric-card">
                <div class="metric-label">Constraint Level</div>
                <div class="metric-value"><span class="badge badge-red">0% Compromise</span></div>
            </div>
            """, unsafe_allow_html=True)
        
        # Main Content
        st.markdown(evidence)
        st.markdown("---")
        st.markdown(experiments)
        
        st.markdown("---")
        st.markdown("## 3. Submit Evaluation")
        st.markdown("As a human expert, rank the options below based on the mathematical/biochemical constraints provided in the evidence.")
        
        with st.form("evaluation_form"):
            col1, col2 = st.columns(2)
            with col1:
                rank1 = st.selectbox("Top Choice (Rank 1)", ["Option A", "Option B", "Option C", "Option D"])
                rank2 = st.selectbox("Rank 2", ["Option A", "Option B", "Option C", "Option D"])
            with col2:
                rank3 = st.selectbox("Rank 3", ["Option A", "Option B", "Option C", "Option D"])
                rank4 = st.selectbox("Rank 4", ["Option A", "Option B", "Option C", "Option D"])
                
            rationale = st.text_area("Rationale for Top Choice (Max 150 words)")
            
            submitted = st.form_submit_button("Submit Evaluation")
            
            if submitted:
                # Save to CSV
                results_dir = Path("data/results")
                results_dir.mkdir(parents=True, exist_ok=True)
                csv_path = results_dir / "expert_scores.csv"
                
                new_data = pd.DataFrame([{
                    "case_id": case_id,
                    "rank_1": rank1,
                    "rank_2": rank2,
                    "rank_3": rank3,
                    "rank_4": rank4,
                    "rationale": rationale
                }])
                
                if csv_path.exists():
                    existing = pd.read_csv(csv_path)
                    updated = pd.concat([existing, new_data], ignore_index=True)
                    updated.to_csv(csv_path, index=False)
                else:
                    new_data.to_csv(csv_path, index=False)
                    
                st.success(f"Evaluation for {case_id} submitted successfully! Saved to {csv_path}")

with tab2:
    st.markdown("## Phase R3: Multi-Agent Scaled Discovery")
    st.markdown("This dashboard displays the automated aggregated metrics from the R3 compartmentalized architecture (Constraint Validator, Scaled Runner, Failure Genomics, Calibration, and Transfer Analysis).")
    
    report_path = Path("tests/evaluation/results/r3_final_report.json")
    if not report_path.exists():
        st.info("R3 Scaled Results not found. Run the scaled discovery pipeline first.")
    else:
        import json
        with open(report_path, 'r', encoding='utf-8') as f:
            r3_data = json.load(f)
            
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Total Cases Evaluated</div>
                <div class="metric-value">{r3_data['meta']['total_cases_evaluated']}</div>
            </div>
            """, unsafe_allow_html=True)
        with m2:
            acc = r3_data['aggregate_metrics']['top1_accuracy']
            color = "green" if acc >= 50 else ("amber" if acc > 20 else "red")
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Generative Accuracy</div>
                <div class="metric-value"><span class="badge badge-{color}">{acc}%</span></div>
            </div>
            """, unsafe_allow_html=True)
        with m3:
            fail_count = r3_data['failure_genomics']['total_failures']
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Failed Hypotheses</div>
                <div class="metric-value">{fail_count}</div>
            </div>
            """, unsafe_allow_html=True)
        with m4:
            ece = r3_data['confidence_calibration']['expected_calibration_error']
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Calibration Error (ECE)</div>
                <div class="metric-value">{ece}</div>
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown("### Failure Genomics Taxonomy")
        
        # Simple bar chart of failure modes
        import altair as alt
        
        fail_dist = r3_data['failure_genomics']['distribution_pct']
        if sum(fail_dist.values()) > 0:
            df_fails = pd.DataFrame([{"Failure Mode": k, "Percentage": v} for k, v in fail_dist.items() if v > 0])
            chart = alt.Chart(df_fails).mark_bar().encode(
                x='Percentage:Q',
                y=alt.Y('Failure Mode:N', sort='-x'),
                color=alt.Color('Failure Mode:N', legend=None),
                tooltip=['Failure Mode', 'Percentage']
            ).properties(height=300)
            st.altair_chart(chart, use_container_width=True)
        else:
            st.success("No failures recorded! 100% Accuracy.")
            
        st.markdown("### Cross-Domain Transfer Analysis")
        transfer = r3_data['cross_domain_transfer']
        st.info(f"The system detected **{transfer.get('cross_domain_retrievals_detected', 0)}** cross-domain memory retrievals from ChromaDB. Transfer Efficiency: **{transfer.get('transfer_efficiency', 0.0):.1%}**.")



