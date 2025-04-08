import streamlit as st
import requests

# Load the Hugging Face token securely
HF_TOKEN = st.secrets["huggingface"]["token"]
API_URL = "https://api-inference.huggingface.co/models/openai-community/gpt2-large"


headers = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "application/json"
}

# Function to get recommendations from LLM based on input
def get_recommendation(industry, product_objective):
    prompt = ("Suggest 2-3 AI/ML models or APIs suitable for Improve Fraud Detection in the Finance industry.\n"
              "- **Model:** Isolation Forest\n"
              "  **Purpose:** Detects anomalies in transaction data\n"
              "  **Tools:** Scikit-learn, AWS Fraud Detector\n"
              "- **Model:** AutoEncoder Neural Networks\n"
              "  **Purpose:** Identifies outliers in high-dimensional data\n"
              "  **Tools:** TensorFlow, PyTorch\n\n"
              f"Now suggest for {product_objective} in the {industry} industry:\n")
    # response = llm(prompt, max_length=250, num_return_sequences=1)
    # return response[0]['generated_text']
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
        recommendations = get_recommendation(industry, product_objective)
    st.subheader(f"Recommended Models/APIs for {product_objective} in {industry}:")
    st.write(recommendations)

st.write("### About the Tool")
st.write("This tool uses the gpt2 model to generate recommendations for AI/ML models or APIs based on the selected industry and use case.")
