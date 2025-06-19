import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

# if len(sys.argv) == 2:
try:
    prompt = sys.argv[1]
except:
    sys.exit("Error: no prompt")

messages = [types.Content(role="user", parts=[types.Part(text=prompt)])]

client_response = client.models.generate_content(model="gemini-2.0-flash-001", contents=messages)

print(client_response.text)
print(f"Prompt tokens: {client_response.usage_metadata.prompt_token_count}")
print(f"Response tokens: {client_response.usage_metadata.candidates_token_count}")
