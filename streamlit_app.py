import streamlit as st
import openai

st.set_page_config(page_title="AI Resume Screener", page_icon="📄")
st.title("📄 AI Resume Screener")
st.write("Paste a job description and your resume to get an instant match score and feedback.")

api_key = st.text_input("Enter your OpenAI API Key", type="password")
job_desc = st.text_area("Paste Job Description Here", height=200)
resume   = st.text_area("Paste Your Resume Here", height=200)

if st.button("Analyze Match"):
    if not api_key:
        st.error("Please enter your OpenAI API key.")
    elif not job_desc or not resume:
        st.error("Please fill in both fields.")
    else:
        with st.spinner("Analyzing your resume..."):
            client = openai.OpenAI(api_key=api_key)
            prompt = f"""
You are a professional resume coach and ATS expert.

Given this job description:
{job_desc}

And this resume:
{resume}

Please provide:
1. A match score out of 100
2. Top 5 keywords MISSING from the resume
3. Top 3 specific suggestions to improve the resume for this role
4. One sentence summary of overall fit

Format your response clearly with headers for each section.
"""
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )
            result = response.choices[0].message.content
            st.success("Analysis Complete!")
            st.markdown(result)
