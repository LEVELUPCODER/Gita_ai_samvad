import os
import requests
import json
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

# 1. Configuration
API_KEY = "AIzaSyDHZGqg87YowhuTHnHEA7HI85JNeg2IHUo"

# 2. Load the "Brain" (Vector DB)
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vector_db = Chroma(persist_directory="gita_db", embedding_function=embeddings)

print("\n--- Gita-AI Samvad (Gemini 2.5 Edition) is Live! ---")
print("Type 'exit' to quit.\n")

while True:
    user_input = input("Amit, tell me what is bothering you today: ")
    if user_input.lower() == 'exit':
        break
    
    print("\nConsulting the Shlokas...")
    
    # Retrieve relevant verses
    docs = vector_db.similarity_search(user_input, k=2)
    context_text = "\n".join([d.page_content for d in docs])
    
    # The Prompt Template
    prompt_text = f"""
    You are Lord Krishna. Guide the youngster Amit using the Bhagavad Gita.
    
    Context (Gita Verses):
    {context_text}
    
    Amit's Problem:
    {user_input}
    
    Your Divine Guidance:"""

    try:
        # THE FIX: Using 'v1beta' and 'gemini-2.5-flash' from your list
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"
        
        payload = {
            "contents": [{
                "parts": [{"text": prompt_text}]
            }]
        }
        
        headers = {'Content-Type': 'application/json'}
        
        # Making the POST request
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        res_json = response.json()

        if response.status_code == 200:
            # Extracting the text
            if 'candidates' in res_json and res_json['candidates']:
                answer = res_json['candidates'][0]['content']['parts'][0]['text']
                print(f"\nKrishna: {answer}\n")
                print("-" * 50)
            else:
                print("\nKrishna is silent (No content returned).")
        else:
            # Error handling
            error_msg = res_json.get('error', {}).get('message', 'Unknown Error')
            print(f"\nAPI Error {response.status_code}: {error_msg}")
            
    except Exception as e:
        print(f"\nSystem Error: {e}")