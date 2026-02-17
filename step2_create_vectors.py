import pandas as pd
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
import os

# 1. Load Data
df = pd.read_csv('data/bhagavad-gita.csv')

# 2. Prepare Data for the AI
# We combine metadata with the translation so the AI knows which verse is which
df['full_context'] = df.apply(lambda x: f"{x['chapter_number']} ({x['chapter_title']}), Verse {x['chapter_verse']}: {x['translation']}", axis=1)

documents = df['full_context'].tolist()

# 3. Initialize the Embedding Model
# This model turns English text into numbers (vectors)
print("Loading Embedding Model (this may take a minute)...")
model_name = "all-MiniLM-L6-v2"
embeddings = HuggingFaceEmbeddings(model_name=model_name)

# 4. Create and Save Vector Database
print("Creating Vector Brain... Converting 640 verses to math...")
persist_directory = "gita_db"

vector_db = Chroma.from_texts(
    texts=documents,
    embedding=embeddings,
    persist_directory=persist_directory
)

print(f"Success! Vector Brain saved in folder: {persist_directory}")