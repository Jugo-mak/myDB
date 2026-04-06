import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def test_model(name):
    print(f"Testing model: {name}")
    try:
        model = genai.GenerativeModel(name)
        response = model.generate_content("hi")
        print(f"  SUCCESS: {response.text[:20]}...")
        return True
    except Exception as e:
        print(f"  ERROR: {e}")
        return False

print("--- FACT CHECK: QUOTA STATUS ---")
flash_ok = test_model("models/gemini-3-flash-preview")
pro_ok = test_model("models/gemini-3.1-pro-preview")
print("--------------------------------")

if flash_ok and pro_ok:
    print("BOTH models are available.")
elif flash_ok:
    print("FLASH is AVAILABLE, PRO is potentially exhausted.")
elif pro_ok:
    print("PRO is AVAILABLE, FLASH is potentially exhausted.")
else:
    print("BOTH models seem to be unavailable or erroring.")
