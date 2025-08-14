# ui/dashboard.py
import streamlit as st
from data.storage import to_dataframe, save_last_session, load_last_session, load_csv
from core.workflow import generate_founders

def make_clickable(url: str, text: str) -> str:
    if not url or not isinstance(url, str):
        return ""
    return f"[{text}]({url})"

def render():
    st.title("🚀 Future Founder Radar — Helsinki")
    st.caption("Archetype-aware scouting: Commercial, Technical, Domain — recall vs precision modes.")

    existing_df = load_last_session()

    with st.sidebar:
        st.header("Settings")
        archetype = st.radio("Archetype", ["Commercial","Technical","Domain"], index=0, horizontal=True)
        recall_mode = st.selectbox("Recall mode", ["precision","balanced","recall"], index=1,
                                   help="Precision: fewer but stronger. Recall: wider net. Balanced: in between.")
        num = st.slider("Leads to generate", 5, 60, 20, help="Upper bound; dedupe may reduce final count.")
        st.caption("SERP requires SERPER_API_KEY. Without it, sample seeds are used.")
        run = st.button("Generate Leads")

    with st.expander("How scoring works"):
        st.markdown("""
- **Commercial:** looks for growth/sales/ARR/enterprise/partnerships signals.
- **Technical:** looks for CTO/staff/principal, ML/AI/infra/distributed/OSS signals.
- **Domain:** looks for Head/Director/GM roles in regulated/deep industries (healthcare, fintech, energy, etc.).
> The table's **Score** reflects matched signals; **Notes** include a brief 'Score why'.
        """.strip())

    if run:
        founders = generate_founders(limit=num, live=True, archetype=archetype, recall_mode=recall_mode)
        df = to_dataframe(founders)

        # keep 'LinkedIn' as raw URL for now (data_editor won't render markdown as link)
        save_last_session(df)
        st.success(f"Generated {len(df)} leads for {archetype} — mode: {recall_mode}")

    elif not existing_df.empty:
        st.info("Loaded your last session.")
        df = existing_df
    else:
        st.info("Click **Generate Leads** to run. If no SERPER key, you’ll see sample seeds. You can also load a CSV.")
        try:
            df = load_csv("assets/sample_founders.csv")
        except Exception:
            st.warning("Add assets/sample_founders.csv to preview sample data.")
            df = None

    if df is not None and not df.empty:
        st.subheader("📋 Founder Pipeline")
        edited_df = st.data_editor(df, use_container_width=True, num_rows="dynamic")
        if st.button("💾 Save Changes"):
            save_last_session(edited_df)
            st.success("Changes saved!")
        st.download_button("⬇ Download CSV", edited_df.to_csv(index=False), "founder_radar.csv", "text/csv")
