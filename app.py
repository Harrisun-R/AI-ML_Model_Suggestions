import streamlit as st
import requests
import re

# Load the Hugging Face token securely
HF_TOKEN = st.secrets["huggingface"]["token"]
API_URL = "https://api-inference.huggingface.co/models/openai-community/gpt2"


headers = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "application/json"
}

def clean_output(text):
    # Only keep lines starting with Model, Purpose, Tools
    lines = text.split("\n")
    cleaned_lines = [line for line in lines if re.match(r"^(Model|Purpose|Tools):", line.strip())]
    return "\n".join(cleaned_lines)

# Function to get recommendations from LLM based on input
def query_huggingface(industry, product_objective):
    prompt = (f"Suggest 2 to 3 AI or ML models or APIs suitable for {product_objective} in the {industry} industry. "
              f"For each, include the model or API name, its purpose in one sentence, and the tools or libraries that can be used. "
              f"Be concise. Do not include extra explanations or repeat the question.")
    payload = {
        "inputs": prompt,
        "parameters": {"max_new_tokens": 300, "temperature": 0.9},
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()[0]["generated_text"]
    else:
        return f"Error: {response.status_code} - {response.text}"

# Placeholder for your name and LinkedIn profile
NAME = "Harrisun Raj Mohan"
LINKEDIN_URL = "https://www.linkedin.com/in/harrisun-raj-mohan/"

# Streamlit App
st.title("AI/ML Decision Support Tool (LLM-based)")
st.write(f"Developed by {NAME}")
st.write(f"[Connect on LinkedIn]({LINKEDIN_URL})")

st.header("Industry and Use Case Selection")
industry = st.selectbox("Select Industry", ["Finance", "Healthcare", "E-commerce", "Manufacturing"])
product_objective = st.selectbox("Select Product Objective", ["Improve Fraud Detection", "Enhance Credit Scoring", 
                                                             "Predict Diseases", "Optimize Medical Imaging", 
                                                             "Build Recommendation Systems", "Segment Customers", 
                                                             "Enable Predictive Maintenance", 
                                                             "Optimize Supply Chain"])

# Generate recommendations from the LLM
if st.button("Recommend AI/ML Models/APIs"):
    with st.spinner('Fetching recommendations...'):
        result = clean_output(query_huggingface(industry, product_objective))
    st.subheader(f"Recommended Models/APIs for {product_objective} in {industry}:")
    st.write(result)

st.write("### About the Tool")
st.write("This tool uses the gpt2 model to generate recommendations for AI/ML models or APIs based on the selected industry and use case.")
