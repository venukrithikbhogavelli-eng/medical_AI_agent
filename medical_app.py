# import streamlit as st
# import google.generativeai as genai
# from PIL import Image
# from pypdf import PdfReader
# import os

# # 1. Setup API Key 
# # PRO TIP: For a hackathon, you can use st.sidebar.text_input for the key to be extra safe!
# API_KEY = "AIzaSyAtsprJlLf2_nO_7d5i1uMJct0IOyE_MCY" 
# genai.configure(api_key=API_KEY)

# # --- 2. THE ERROR RESOLVER: Dynamic Model Selection ---
# def get_best_model():
#     """Queries the API to find the newest available model to avoid 404s"""
#     try:
#         models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
#         # In March 2026, we want Gemini 3 or 2.5
#         for preferred in ["models/gemini-3-flash-preview", "models/gemini-2.5-flash", "models/gemini-2.0-flash"]:
#             if preferred in models:
#                 return preferred
#         return models[0] # Fallback to whatever is active
#     except Exception:
#         return "gemini-2.5-flash" # Hardcoded backup

# ACTIVE_MODEL = get_best_model()

# # --- 3. UI LAYOUT ---
# st.set_page_config(page_title="MedScan AI Agent", page_icon="🏥", layout="wide")

# st.title("🏥 MedScan: Clinical Correlation Agent")
# st.markdown(f"**Current Brain:** `{ACTIVE_MODEL}`")

# # Create two columns for the Uploaders
# col1, col2 = st.columns(2)

# with col1:
#     st.subheader("📸 Medical Scan")
#     uploaded_image = st.file_uploader("Upload X-Ray, MRI, or CT Scan", type=["jpg", "jpeg", "png"])
#     if uploaded_image:
#         st.image(uploaded_image, caption="Uploaded Scan", use_container_width=True)

# with col2:
#     st.subheader("📄 Lab Report")
#     uploaded_pdf = st.file_uploader("Upload Blood Test or Report (PDF)", type=["pdf"])
#     if uploaded_pdf:
#         st.success("✅ PDF Processed")

# # --- 4. CORE LOGIC ---
# # Button is enabled only if at least one file is uploaded
# if uploaded_image or uploaded_pdf:
#     if st.button("🚀 Run Agentic Analysis", type="primary", use_container_width=True):
#         try:
#             with st.spinner("Analyzing data..."):
#                 input_data = []
#                 context_text = ""

#                 # Extract Text from PDF if exists
#                 if uploaded_pdf:
#                     reader = PdfReader(uploaded_pdf)
#                     pdf_text = " ".join([page.extract_text() for page in reader.pages])
#                     context_text += f"\nLAB REPORT DATA: {pdf_text}"

#                 # Add Image if exists
#                 if uploaded_image:
#                     img = Image.open(uploaded_image)
#                     input_data.append(img)
                
#                 # The "Agentic" Medical Prompt
#                 prompt = f"""
#                 You are a Medical Diagnostic AI Agent. 
#                 Context Provided: {context_text if context_text else 'No lab text provided, analyze image only.'}
                
#                 YOUR TASKS:
#                 1. Identify any visual anomalies in the scan.
#                 2. Correlate lab values with the visual findings (if both provided).
#                 3. Structure findings into a 'Risk Assessment' table.
#                 4. List 3 specific clinical questions for a human doctor.
                
#                 IMPORTANT: Start with a clear 'NOT A DIAGNOSIS' disclaimer in bold.
#                 """
#                 input_data.insert(0, prompt)

#                 # Initialize and run the model
#                 model = genai.GenerativeModel(ACTIVE_MODEL)
#                 response = model.generate_content(input_data)
                
#                 st.divider()
#                 st.subheader("🩺 Agent Findings")
#                 st.markdown(response.text)

#         except Exception as e:
#             st.error(f"⚠️ Connection Error: {str(e)}")
#             st.info("Check if your API key is correct in the code.")
# else:
#     st.warning("👈 Please upload a Scan or a PDF Report to start the analysis.")

import streamlit as st
import google.generativeai as genai
from PIL import Image
from pypdf import PdfReader
from gtts import gTTS
import base64
import os

# 1. Setup API Key
API_KEY = "AIzaSyAtsprJlLf2_nO_7d5i1uMJct0IOyE_MCY" 
genai.configure(api_key=API_KEY)

# --- 2. THE ERROR RESOLVER: Finds the newest model automatically ---
def get_working_model():
    try:
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        # In 2026, we check for Gemini 3 or 2.5 series first
        for preferred in ["models/gemini-3-flash", "models/gemini-2.5-flash", "models/gemini-2.0-flash"]:
            if preferred in models:
                return preferred
        return models[0] # Fallback to any available model
    except Exception:
        return "gemini-1.5-flash" # Last resort hardcoded

ACTIVE_MODEL_NAME = get_working_model()

# --- 3. UI SETUP ---
st.set_page_config(page_title="MedScan Agentic AI", page_icon="🩺", layout="wide")

st.title("🏥 MedScan Pro: Agentic Clinical Assistant")
st.markdown(f"**AI Engine Active:** `{ACTIVE_MODEL_NAME}`")

# Sidebar for the "Unique" Features
with st.sidebar:
    st.header("🎯 Agent Intelligence")
    # Feature 3: Persona/Target Audience
    view_mode = st.radio("Who is reading this report?", ["Doctor (Technical)", "Patient (Simple Terms)"])
    st.divider()
    st.info("This agent correlates medical scans with lab data and provides a voice briefing.")

# Upload Columns
c1, c2 = st.columns(2)
with c1:
    uploaded_image = st.file_uploader("Upload Medical Scan (JPG/PNG)", type=["jpg", "jpeg", "png"])
    if uploaded_image:
        st.image(uploaded_image, caption="Uploaded Scan", use_container_width=True)

with c2:
    uploaded_pdf = st.file_uploader("Upload Lab Report (PDF)", type=["pdf"])
    if uploaded_pdf:
        st.success("Lab Report Received")

# --- 4. CORE LOGIC ---
if uploaded_image or uploaded_pdf:
    if st.button("🚀 Run Clinical Analysis", type="primary", use_container_width=True):
        try:
            with st.spinner("Processing medical data..."):
                input_data = []
                
                # Extract PDF text if provided
                pdf_context = ""
                if uploaded_pdf:
                    reader = PdfReader(uploaded_pdf)
                    pdf_context = " ".join([page.extract_text() for page in reader.pages])

                # Build the Prompt based on the Persona (Feature 3)
                persona_instruction = (
                    "Use high-level clinical terminology, ICD-10 codes, and physiological markers." 
                    if view_mode == "Doctor (Technical)" else 
                    "Use simple, comforting language. Explain medical terms like you are talking to a non-expert."
                )

                prompt = f"""
                You are a Senior Medical AI Agent.
                TARGET AUDIENCE: {view_mode}
                INSTRUCTION: {persona_instruction}
                
                LAB DATA: {pdf_context if pdf_context else 'Not provided'}
                
                TASK:
                1. Analyze the scan for anomalies.
                2. Correlate blood/lab values with the visual scan.
                3. Create a 'Summary' and 'Suggested Next Steps'.
                4. End with a 2-sentence 'Verbal Briefing' for a quick audio summary.
                
                DISCLAIMER: State clearly this is not a final medical diagnosis.
                """

                # Prepare Multimodal Input
                input_data.append(prompt)
                if uploaded_image:
                    input_data.append(Image.open(uploaded_image))

                # Generate Response
                model = genai.GenerativeModel(ACTIVE_MODEL_NAME)
                response = model.generate_content(input_data)
                full_text = response.text

                # Display Text Report
                st.divider()
                st.subheader(f"📋 {view_mode} Report")
                st.markdown(full_text)

                # --- 5. VOICE BRIEFING (Feature 1) ---
                st.divider()
                st.subheader("🔊 Audio Clinical Briefing")
                # We take the last 300 characters or a summary portion for the audio
                audio_text = f"Analysis complete for {view_mode}. " + full_text[:400]
                tts = gTTS(text=audio_text, lang='en')
                tts.save("briefing.mp3")
                
                with open("briefing.mp3", "rb") as f:
                    audio_bytes = f.read()
                b64 = base64.b64encode(audio_bytes).decode()
                audio_html = f'<audio controls src="data:audio/mp3;base64,{b64}"></audio>'
                st.markdown(audio_html, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Error: {e}")
else:
    st.info("Please upload a file to begin.")