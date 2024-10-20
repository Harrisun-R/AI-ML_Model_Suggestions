import streamlit as st
from transformers import pipeline

# Load the LLM from Hugging Face
@st.cache(allow_output_mutation=True)
def load_model():
    return pipeline("text-generation", model="EleutherAI/gpt-neo-125M")

llm = load_model()

# Function to get recommendations from LLM based on input
def get_recommendation(industry, use_case):
    prompt = (f"Recommend the best AI/ML models or APIs for {use_case} in the {industry} industry."
              f" Provide the model name, a brief description, and suggested APIs or Tools"
    response = llm(prompt, max_length=200, num_return_sequences=1)
    return response[0]['generated_text']

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
        recommendations = get_recommendation(industry, use_case)
    st.subheader(f"Recommended Models/APIs for {use_case} in {industry}:")
    st.write(recommendations)

st.write("### About the Tool")
st.write("This tool uses an open-source LLM to generate recommendations for AI/ML models or APIs based on the selected industry and use case.")
