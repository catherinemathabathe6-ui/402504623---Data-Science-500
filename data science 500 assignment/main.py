import os
import pandas as pd

from scraper import scrape_books
from cleaner import clean_data
from visualization import visualize_data
from model import build_model

print("BOOK MARKET ANALYTICS PROJECT")

if os.path.exists("raw_books.csv"):
    df_raw = pd.read_csv("raw_books.csv")
    print(f"Loaded existing raw_books.csv ({len(df_raw)} books)")
else:
    df_raw = scrape_books()

df_clean = clean_data(df_raw)

visualize_data(df_clean)
model, X_model, results, coefficients = build_model(df_clean)

print("PROJECT COMPLETE")