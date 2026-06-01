from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

def get_health_remarks(glucose, haemoglobin, cholesterol):
    try:
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": f"""You are a medical AI assistant. Based on the following 
                    blood test results, provide a health assessment in this exact format:

🔍 HEALTH SUMMARY:
Write 1 sentence overall health summary here.

⚠️ RISK FACTORS:
- Write risk factor 1
- Write risk factor 2

✅ RECOMMENDATIONS:
- Write recommendation 1
- Write recommendation 2

Blood Test Results:
- Glucose: {glucose} mg/dL
- Haemoglobin: {haemoglobin} g/dL
- Cholesterol: {cholesterol} mg/dL"""
                }
            ]
        )
        return response.choices[0].message.content
    
    except Exception as e:
        return f"Unable to generate remarks: {str(e)}"