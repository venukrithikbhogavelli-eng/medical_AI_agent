I’ve built MedScan AI, an agentic system designed to solve the 'Data Silo' problem in hospitals.

Instead of just analyzing an image, my agent performs Clinical Correlation. It reads the patient's blood work from a PDF and compares it against their MRI scan in real-time to find inconsistencies.

To make it practical, it features a Multi-Persona engine—it can brief a surgeon using technical terminology or explain the results to a patient in simple language. We’ve even included a Voice Briefing module for hands-free clinical environments. It’s not just a tool; it’s a virtual member of the diagnostic team."


1. Create a venv environment for python

2. Install all these packages-
  pip install --upgrade google-generativeai pypdf pillow streamlit gTTS

3. Run the code
   streamlit run medical_app.py



