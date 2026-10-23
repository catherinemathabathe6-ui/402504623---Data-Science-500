import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LinearRegression
from sklearn.dummy import DummyRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

def build_model(df, min_genre_size=10):

    data = df.copy()

    counts = data["Category"].value_counts()
    rare = counts[counts < min_genre_size].index
    data["Category_Grouped"] = data["Category"].replace(dict.fromkeys(rare, "Other"))

    numeric_features = ["Rating", "Stock_Quantity", "Num_Reviews",
                        "Description_Word_Count", "Title_Length", "Has_Description"]

    numeric_features = [c for c in numeric_features if data[c].nunique() > 1]
    print("Numeric features used:", numeric_features)

    X = pd.get_dummies(data[numeric_features + ["Category_Grouped"]],
                       columns=["Category_Grouped"], drop_first=True, dtype=int)
    y = data["Price"]
    print("Modelling dataset shape:", X.shape)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    baseline = DummyRegressor(strategy="mean").fit(X_train, y_train)
    base_predict = baseline.predict(X_test)

    model = LinearRegression()
    model.fit(X_train, y_train)
    predict = model.predict(X_test)

    def metrics(y_true, y_predict):
        mse = mean_squared_error(y_true, y_predict)
        return {"MAE": mean_absolute_error(y_true, y_predict),
                "RMSE": np.sqrt(mse),
                "R2": r2_score(y_true, y_predict)}

    results = pd.DataFrame({"Baseline (mean)": metrics(y_test, base_predict),
                            "Linear Regression": metrics(y_test, predict)}).T
    print("\nMODEL RESULTS (test set)")
    print(results.round(3))

    cv_r2 = cross_val_score(LinearRegression(), X, y, cv=5, scoring="r2")
    print(f"\n5-fold CV R2: mean = {cv_r2.mean():.3f}, std = {cv_r2.std():.3f}")
    print(f"Train R2: {model.score(X_train, y_train):.3f} | "
          f"Test R2: {model.score(X_test, y_test):.3f}")

    coefficients = pd.Series(model.coef_, index=X.columns).sort_values(key=abs, ascending=False)
    print("\nTop 10 coefficients (by size):")
    print(coefficients.head(10).round(3))
    print("Intercept:", round(model.intercept_, 3))

    fig, axes = plt.subplots(1, 2, figsize=(13, 5))

    axes[0].scatter(y_test, predict, alpha=0.5)
    lims = [y.min(), y.max()]
    axes[0].plot(lims, lims, "r--", label="Perfect prediction")
    axes[0].set_xlabel("Actual Price (GBP)")
    axes[0].set_ylabel("Predicted Price (GBP)")
    axes[0].set_title("Actual vs Predicted Prices")
    axes[0].legend()

    residuals = y_test - predict
    axes[1].scatter(predict, residuals, alpha=0.5)
    axes[1].axhline(0, color="red", linestyle="--")
    axes[1].set_xlabel("Predicted Price (GBP)")
    axes[1].set_ylabel("Residual (Actual - Predicted)")
    axes[1].set_title("Residual Plot")

    plt.tight_layout()
    plt.show()

    return model, X, results, coefficients