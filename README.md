# Data Science 500 Assignment
GitHub repository:
https://github.com/catherinemathabathe6-ui/402504623---Data-Science-500
402504623-DataScience500

# Project Overview

This data science project is an end-to-end pipeline that scrapes book data from an online bookstore simulator ("Books to Scrape"), cleans and preprocesses the data, performs exploratory data analysis through visualizations, and trains a predictive machine learning model to estimate book prices based on features like category, rating, and description length.



# Project Structure & File Breakdown

- **`main_2.py`**: The core control script that coordinates the entire workflow—checking for existing raw data, triggering data scraping if needed, running data cleaning, generating visualizations, and training the predictive model[cite: 8].
- **`scraper.py`**: Uses `requests` and `BeautifulSoup` to scrape book listings and detailed product pages (extracting titles, prices, star ratings, stock availability, UPC, review counts, and descriptions) and saves the raw output to `raw_books.csv`[cite: 10].
- **`cleaner.py`**: Cleans the raw dataset by removing duplicate UPCs[cite: 7], converting prices and ratings into usable numeric formats[cite: 7], handling missing stock quantities and descriptions[cite: 7], and exporting the final data to `cleaned_books.csv`[cite: 7].
- **`visualization.py`**: Uses `matplotlib` and `seaborn` to generate visual insights, including price distributions, rating counts, price-by-rating boxplots, top category comparisons, stock status comparisons, and correlation heatmaps[cite: 11].
- **`model.py`**: Prepares features (including one-hot encoded grouped categories and numeric metrics), splits the data for training and testing, and builds a **Linear Regression** model compared against a **Dummy Regressor** baseline, evaluating performance using MAE, RMSE, R2 score, cross-validation, and residual plots[cite: 9].


# Main Features

- **Automated Web Scraping:** Extracts multi-page catalog data and handles individual product detail pages with built-in delays to respect server limits[cite: 10].
- **Data Cleaning:** Standardizes text using regular expressions[cite: 7], fills missing numerical fields with medians[cite: 7], and filters out invalid pricing or missing core metadata[cite: 7].
- **Exploratory Data Analysis:** Visualizes underlying trends, pricing distributions, genre statistics, and correlations between book characteristics[cite: 11].
- **Machine Learning & Evaluation:** Predicts book prices using a trained Linear Regression model, backed by 5-fold cross-validation and actual vs. predicted residual plots[cite: 9].




# How to Run

Execute the main controller script in your IDE :

##
python main_2.py
##
