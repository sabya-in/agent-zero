import os
from google import genai

# The client gets the API key from the environment variable `GEMINI_API_KEY`.
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("Please set the GOOGLE_API_KEY environment variable.")

client = genai.Client(api_key=api_key)

prompt = input("Ask Gemini something: ")

response = client.models.generate_content(
    model="gemini-2.5-flash", contents=prompt
)
print(response.text)