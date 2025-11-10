# app.py
import streamlit as st
from data import MESSY_CHAT_THREAD, GOLDEN_TASKS
from agent import v1_naive, v2_orchestrated


# 1. Configure page specifically for a wide demo view
st.set_page_config(layout="wide", page_title="Agent Evals Demo")

# 2. Header - The "Why" of this demo
st.title("Iterative Agent Development: Task Extraction")
st.markdown("""
**The Goal:** Build an agent that correctly extracts structured tasks from messy human chat.
**The Process:** We start with V1, analyze its failures (loss analysis), and hill-climb to a better version""")

# 3. Main Interface - Two Column Layout
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Sprint Planning Chat")
    #Displaying the raw data so the audience sees the challenge
    st.text_area("Chat Log", MESSY_CHAT_THREAD, height=400, disabled=True)

with col2:
    st.subheader("Agent Output")

    # THe core demo control: Switching between model versions
    version = st.radio("Select Agent Version",
                       ["V1 (Zero-Shot)", "V2 (Orchestrated Chain-of-Thought)"],
                       horizontal=True)

    if st.button(f"Run {version}", type="primary"):
        with st.spinner("Analyzing dependencies..."):
            if "V1" in version:
                st.json(v1_naive(MESSY_CHAT_THREAD))
            else:
                result = v2_orchestrated(MESSY_CHAT_THREAD)
                with st.expander("View Dependency Analysis (Hill-Climbing)", expanded=True):
                    st.write(result["reasoning"])
                st.subheader("Final Extracted Tasks")
                st.json(result["tasks"])

st.divider()
st.header("Golden Dataset (Ground Truth)")
st.json(GOLDEN_TASKS)