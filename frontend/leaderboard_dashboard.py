import streamlit as st
import pandas as pd
import json
import os
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Antigravity Leaderboard", layout="wide")

st.title("🌌 Antigravity ConstraintBench v1.0")
st.subheader("Global Reproduction Leaderboard & Evidence Consolidation")

st.markdown("""
This dashboard visualizes **Phase 6: Evidence Consolidation**. It aggregates external, independent reproductions of the temporal leakage effect across various models and hardware configurations.
""")

data_path = os.path.join(os.path.dirname(__file__), "..", "data", "ANTIGRAVITY_EVIDENCE_V1", "community_evidence.json")

if not os.path.exists(data_path):
    st.error("No community evidence found. Run `ingest_reproductions.py` first.")
else:
    with open(data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    if not data:
        st.warning("Community evidence database is empty.")
    else:
        df = pd.DataFrame(data)
        
        # Display high-level metrics
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Reproductions", len(df))
        col2.metric("Unique Models Evaluated", df['model'].nunique())
        col3.metric("Avg Global Leakage", f"{df['leakage_rate'].mean():.1f}%")
        
        st.markdown("---")
        
        # Model Leaderboard
        st.subheader("🏆 Model Leaderboard")
        st.markdown("Ranked by average leakage (lower is better, meaning higher resistance to temporal contamination).")
        
        leaderboard = df.groupby('model').agg(
            Evaluations=('reviewer', 'count'),
            Avg_Leakage=('leakage_rate', 'mean'),
            Min_Leakage=('leakage_rate', 'min'),
            Max_Leakage=('leakage_rate', 'max')
        ).reset_index().sort_values(by='Avg_Leakage', ascending=True)
        
        leaderboard['Avg_Leakage'] = leaderboard['Avg_Leakage'].map('{:.1f}%'.format)
        leaderboard['Min_Leakage'] = leaderboard['Min_Leakage'].map('{:.1f}%'.format)
        leaderboard['Max_Leakage'] = leaderboard['Max_Leakage'].map('{:.1f}%'.format)
        
        st.dataframe(leaderboard, use_container_width=True)
        
        # Visualizations
        st.markdown("---")
        st.subheader("📊 Leakage Distribution by Model")
        
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.boxplot(data=df, x='leakage_rate', y='model', ax=ax, palette='viridis')
        ax.set_xlabel("Temporal Leakage Rate (%)")
        ax.set_ylabel("")
        st.pyplot(fig)
        
        # Reproduction Outcomes
        st.markdown("---")
        st.subheader("🔬 Reproduction Outcomes")
        outcome_counts = df['outcome'].value_counts()
        fig2, ax2 = plt.subplots()
        ax2.pie(outcome_counts, labels=outcome_counts.index, autopct='%1.1f%%', colors=sns.color_palette('pastel'))
        st.pyplot(fig2)
