import requests
import os

# Your API Key
API_KEY = "AIzaSyDHZGqg87YowhuTHnHEA7HI85JNeg2IHUo"

# We check the 'v1beta' endpoint because that is where most free-tier models live
url = f"https://generativelanguage.googleapis.com/v1beta/models?key={API_KEY}"

print(f"Checking available models for key ending in ...{API_KEY[-4:]}")

try:
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        print("\n--- AVAILABLE MODELS ---")
        found_any = False
        for model in data.get('models', []):
            # We only care about models that can generate text (generateContent)
            if "generateContent" in model.get('supportedGenerationMethods', []):
                print(f"Name: {model['name']}") # This is the exact string we need
                found_any = True
        
        if not found_any:
            print("No models found that support 'generateContent'.")
    else:
        print(f"Error: {response.status_code}")
        print(response.text)

except Exception as e:
    print(f"Connection failed: {e}")