import pandas as pd
import os

# 1. Path to your file (update the name if yours is different)
file_path = 'data/bhagavad-gita.csv' 

if os.path.exists(file_path):
    df = pd.read_csv(file_path)
    
    print("--- Dataset Info ---")
    print(f"Total Verses: {len(df)}")
    print("\n--- Column Names (Very Important) ---")
    print(df.columns.tolist())
    
    print("\n--- First 2 Rows Preview ---")
    print(df.head(2))
else:
    print(f"Error: File not found at {file_path}. Please check the filename.")