import streamlit as st
import requests
import json
import re

# ----------------------------
# CONFIG: Replace with your API Key
# ----------------------------
OPENROUTER_API_KEY = st.secrets["openrouter"]["api_key"]
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

# Placeholder for your name and LinkedIn profile
NAME = "Harrisun Raj Mohan"
LINKEDIN_URL = "https://www.linkedin.com/in/harrisun-raj-mohan/"

# ----------------------------
# Function to clean AI output
# ----------------------------
def clean_output(text):
    """
    Cleans and formats model output for readability.
    Looks for 'Model', 'Purpose', and 'Tools' sections.
    """
    lines = text.split("\n")
    cleaned = []
    for line in lines:
        if re.match(r"^(Model|Purpose|Tools|Name|API):", line.strip()):
            cleaned.append(line.strip())
    return "\n".join(cleaned) if cleaned else text

# ----------------------------
# Function to call OpenRouter API
# ----------------------------
def query_openrouter(industry, product_objective):
    prompt = (
        f"Suggest 2 or 3 AI or ML models or APIs for **{product_objective}** in the **{industry}** industry.\n\n"
        f"For each recommendation, include:\n"
        f"- Model or API Name\n"
        f"- One-line Purpose\n"
        f"- Relevant Tools or Libraries\n\n"
        f"Keep it short and structured."
    )

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://your-site-url.com",  # Optional
        "X-Title": "AI-ML Decision Support Tool",     # Optional
    }

    payload = {
        "model": "openai/gpt-oss-20b:free",  # free tier model
        "messages": [
            {"role": "system", "content": "You are an AI assistant helping product managers choose AI/ML models."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.8,
        "max_tokens": 400,
    }

    try:
        response = requests.post(OPENROUTER_URL, headers=headers, data=json.dumps(payload))
        if response.status_code == 200:
            data = response.json()
            text = data["choices"][0]["message"]["content"]
            return clean_output(text)
        else:
            return f"❌ Error {response.status_code}: {response.text}"
    except Exception as e:
        return f"⚠️ API Request failed: {str(e)}"

# ----------------------------
# STREAMLIT APP UI
# ----------------------------
st.set_page_config(page_title="AI/ML Decision Support Tool", layout="centered")

st.title("🤖 AI/ML Decision Support Tool")
st.write(f"Developed by **{NAME}** · [LinkedIn]({LINKEDIN_URL})")

st.header("🔍 Industry and Use Case Selection")
industry = st.selectbox("Select Industry", ["Finance", "Healthcare", "E-commerce", "Manufacturing"])
product_objective = st.selectbox("Select Product Objective", [
    "Improve Fraud Detection", "Enhance Credit Scoring",
    "Predict Diseases", "Optimize Medical Imaging",
    "Build Recommendation Systems", "Segment Customers",
    "Enable Predictive Maintenance", "Optimize Supply Chain"
])

# Generate recommendations from OpenRouter LLM
if st.button("🚀 Recommend AI/ML Models/APIs"):
    with st.spinner("Fetching smart recommendations..."):
        result = query_openrouter(industry, product_objective)
    st.subheader(f"📌 Recommended Models/APIs for **{product_objective}** in **{industry}**:")
    st.markdown(result)

# ----------------------------
# About Section
# ----------------------------
st.write("---")
st.write("### ℹ️ About the Tool")
st.info(
    "This tool leverages **OpenRouter LLMs** to suggest AI/ML models and APIs "
    "tailored to specific industries and product objectives. "
    "It enhances product managers' decision-making by offering concise, actionable insights."
)
