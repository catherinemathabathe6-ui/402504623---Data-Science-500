import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid", palette="muted")

def visualize_data(df, top_n=10):

#Price distribution
    plt.figure(figsize=(10, 6))
    sns.histplot(df["Price"], bins=25, kde=True)
    plt.axvline(df["Price"].mean(), color="red", linestyle="--",
                label=f"Mean: £{df['Price'].mean():.2f}")
    plt.axvline(df["Price"].median(), color="green", linestyle="--",
                label=f"Median: £{df['Price'].median():.2f}")
    plt.title("Distribution of Book Prices")
    plt.xlabel("Price (GBP)")
    plt.ylabel("Number of Books")
    plt.legend()
    plt.tight_layout()
    plt.show()

# Rating distribution
    plt.figure(figsize=(8, 5))
    sns.countplot(x="Rating", data=df, order=[1, 2, 3, 4, 5])
    plt.title("Book Rating Distribution")
    plt.xlabel("Star Rating")
    plt.ylabel("Number of Books")
    plt.tight_layout()
    plt.show()

# 3. Price vs rating
    plt.figure(figsize=(8, 5))
    sns.boxplot(x="Rating", y="Price", data=df, order=[1, 2, 3, 4, 5])
    plt.title("Book Price by Star Rating")
    plt.xlabel("Star Rating")
    plt.ylabel("Price (GBP)")
    plt.tight_layout()
    plt.show()

#number of books in the top genres
    top_cats = df["Category"].value_counts().head(top_n)
    plt.figure(figsize=(10, 6))
    sns.barplot(x=top_cats.values, y=top_cats.index)
    plt.title(f"Top {top_n} Genres by Number of Books")
    plt.xlabel("Number of Books")
    plt.ylabel("Genre")
    plt.tight_layout()
    plt.show()

#average price
    cat_stats = df.groupby("Category")["Price"].agg(["mean", "count"])
    cat_stats = cat_stats[cat_stats["count"] >= 10].sort_values("mean", ascending=False)
    plt.figure(figsize=(10, 8))
    sns.barplot(x=cat_stats["mean"].head(15).values,
                y=cat_stats["mean"].head(15).index)
    plt.title("Average Price by Genre (genres with 10+ books, top 15)")
    plt.xlabel("Average Price (GBP)")
    plt.ylabel("Genre")
    plt.tight_layout()
    plt.show()

# average rating
    cat_rating = (df.groupby("Category")["Rating"].agg(["mean", "count"])
                    .query("count >= 10").sort_values("mean", ascending=False))
    plt.figure(figsize=(10, 8))
    sns.barplot(x=cat_rating["mean"].head(15).values,
                y=cat_rating["mean"].head(15).index)
    plt.title("Average Rating by Genre (genres with 10+ books, top 15)")
    plt.xlabel("Average Star Rating")
    plt.ylabel("Genre")
    plt.tight_layout()
    plt.show()

# 7. Price by stock status

    plt.figure(figsize=(7, 5))
    sns.boxplot(x="In_Stock", y="Price", data=df)
    plt.xticks([0, 1], ["Out of stock", "In stock"])
    plt.title("Price by Stock Status")
    plt.xlabel("")
    plt.ylabel("Price (GBP)")
    plt.tight_layout()
    plt.show()

#price and description length
    plt.figure(figsize=(8, 5))
    sns.scatterplot(x="Description_Word_Count", y="Price", data=df, alpha=0.5)
    sns.regplot(x="Description_Word_Count", y="Price", data=df,
                scatter=False, color="red")
    plt.title("Price vs Description Length")
    plt.xlabel("Description Word Count")
    plt.ylabel("Price (GBP)")
    plt.tight_layout()
    plt.show()

#correlation heatmap
    num_cols = ["Price", "Rating", "Stock_Quantity", "Num_Reviews",
                "Description_Word_Count", "Title_Length"]
    plt.figure(figsize=(8, 6))
    sns.heatmap(df[num_cols].corr(), annot=True, fmt=".2f",
                cmap="coolwarm", center=0)
    plt.title("Correlation Between Numeric Variables")
    plt.tight_layout()
    plt.show()

