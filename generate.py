import os
from google import genai

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

def generate_ad_copy(prompt):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response.text