import streamlit as st
import requests
import plotly.graph_objects as go

# Page Configuration
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="🤖",
    layout="wide"
)

# Sidebar
with st.sidebar:
    st.title("🤖 AI Resume Analyzer")

    st.markdown("---")

    st.info("""
### Features

✅ ATS Score

✅ Resume Summary

✅ Skills Analysis

✅ Strengths & Weaknesses

✅ Project Analysis

✅ Certifications

✅ Interview Questions
""")

# Main Header
st.title("🤖 AI Resume Analyzer")
st.caption("Upload your resume and receive AI-powered career insights")

# File Upload
uploaded_file = st.file_uploader(
    "Upload Resume PDF",
    type=["pdf"]
)

if uploaded_file:

    if st.button("Analyze Resume", use_container_width=True):

        with st.spinner("Analyzing Resume..."):

            files = {
                "file": (
                    uploaded_file.name,
                    uploaded_file,
                    "application/pdf"
                )
            }

            try:
                response = requests.post(
                    "http://127.0.0.1:8000/summarize-pdf",
                    files=files
                )

                if response.status_code != 200:
                    st.error("Backend Error")
                    st.code(response.text)
                    st.stop()

                result = response.json()

                st.success("✅ Resume Analysis Completed")

                # ATS Score
                ats_score = result.get("ats_score", 0)

                fig = go.Figure(
                    go.Indicator(
                        mode="gauge+number",
                        value=ats_score,
                        title={"text": "ATS Score"},
                        gauge={
                            "axis": {"range": [0, 100]}
                        }
                    )
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

                # Metrics
                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    st.metric(
                        "ATS Score",
                        f"{ats_score}%"
                    )

                with col2:
                    st.metric(
                        "Skills",
                        len(result.get("skills", []))
                    )

                with col3:
                    st.metric(
                        "Projects",
                        len(result.get("projects", []))
                    )

                with col4:
                    st.metric(
                        "Certifications",
                        len(result.get("certifications", []))
                    )

                st.markdown("---")

                # Tabs
                tab1, tab2, tab3, tab4, tab5 = st.tabs([
                    "📄 Summary",
                    "🛠 Skills",
                    "📂 Projects",
                    "❓ Interview Questions",
                    "📈 Strengths & Weaknesses"
                ])

                # Summary
                with tab1:
                    st.subheader("Professional Summary")

                    st.write(
                        result.get(
                            "professional_summary",
                            "No summary available."
                        )
                    )

                # Skills
                with tab2:
                    st.subheader("Skills")

                    skills = result.get("skills", [])

                    if skills:
                        for skill in skills:
                            st.success(skill)
                    else:
                        st.info("No skills found.")

                # Projects
                with tab3:
                    st.subheader("Projects")

                    projects = result.get("projects", [])

                    if projects:
                        for project in projects:
                            st.info(project)
                    else:
                        st.info("No projects found.")

                # Interview Questions
                with tab4:
                    st.subheader("Interview Questions")

                    questions = result.get(
                        "interview_questions",
                        []
                    )

                    if questions:
                        for i, question in enumerate(
                            questions,
                            start=1
                        ):
                            st.write(
                                f"{i}. {question}"
                            )
                    else:
                        st.info(
                            "No interview questions generated."
                        )

                # Strengths & Weaknesses
                with tab5:

                    col_left, col_right = st.columns(2)

                    with col_left:
                        st.subheader("✅ Strengths")

                        strengths = result.get(
                            "strengths",
                            []
                        )

                        if strengths:
                            for item in strengths:
                                st.success(item)
                        else:
                            st.info(
                                "No strengths available."
                            )

                    with col_right:
                        st.subheader("⚠ Weaknesses")

                        weaknesses = result.get(
                            "weaknesses",
                            []
                        )

                        if weaknesses:
                            for item in weaknesses:
                                st.warning(item)
                        else:
                            st.info(
                                "No weaknesses available."
                            )

                st.markdown("---")

                # Download Report
                st.download_button(
                    label="📥 Download Analysis Report",
                    data=str(result),
                    file_name="resume_analysis.txt",
                    mime="text/plain"
                )

            except Exception as e:
                st.error(f"Error: {str(e)}")