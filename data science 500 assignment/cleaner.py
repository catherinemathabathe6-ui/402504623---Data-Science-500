import re
import pandas as pd

RATING_MAP = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}

def clean_text(text):
    if pd.isna(text) or str(text).strip() == "":
        return ""
    text = str(text).lower()
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    return re.sub(r"\s+", " ", text).strip()

def clean_data(df_raw):
    df = df_raw.copy()
    print("Rows before cleaning:", len(df))

    df = df.drop_duplicates(subset="UPC", keep="first")

    df["Price"] = (
        df["Price"].astype(str).str.extract(r"(\d+\.?\d*)")[0].astype(float)
    )

    df["Rating"] = df["Rating"].map(RATING_MAP)

    df["Stock"] = df["Stock"].astype(str).str.strip()
    df["In_Stock"] = df["Stock"].str.lower().str.contains("in stock").astype(int)

    df["Stock_Quantity"] = pd.to_numeric(df["Stock_Quantity"], errors="coerce")
    df["Num_Reviews"] = pd.to_numeric(df["Num_Reviews"], errors="coerce")

    df.loc[df["In_Stock"] == 0, "Stock_Quantity"] = 0
    median_qty = df.loc[df["In_Stock"] == 1, "Stock_Quantity"].median()
    df["Stock_Quantity"] = df["Stock_Quantity"].fillna(median_qty)
    df["Num_Reviews"] = df["Num_Reviews"].fillna(0)

    df["Title"] = df["Title"].astype(str).str.strip()
    df["Category"] = df["Category"].astype(str).str.strip()
    df["Has_Description"] = df["Description"].notna().astype(int)
    df["Description_Clean"] = df["Description"].apply(clean_text)
    df["Description_Word_Count"] = df["Description_Clean"].str.split().str.len()
    df["Title_Length"] = df["Title"].str.len()

    df = df.dropna(subset=["Title", "Price", "Rating", "Category"])
    df = df[df["Price"] > 0]

    df = df.reset_index(drop=True)

    print("Rows after cleaning:", len(df))
    print("\nMissing values per column:")
    print(df.isna().sum())
    print("\nData types:")
    print(df.dtypes)

    df.to_csv("cleaned_books.csv", index=False)
    print("\nCleaned dataset saved.")
    return df
