import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.preprocessing import LabelEncoder

# -------- LOAD FILES -------- #
# Adjust paths as needed
behavior_df = pd.read_csv("wallet_behavior_details.csv")
scores_df = pd.read_csv("wallet_scores.csv")

# -------- PREPROCESSING -------- #
# Merge both dataframes on wallet address
df = pd.merge(behavior_df, scores_df, on="wallet")

# Convert 'liquidated' from bool/str to int
if df['liquidated'].dtype != 'int':
    df['liquidated'] = df['liquidated'].astype(str).str.lower().map({'true': 1, 'false': 0})

# -------- FEATURES & TARGET -------- #
feature_cols = ['total_deposit', 'total_withdraw', 'total_borrow', 'total_repay', 'liquidated']
X = df[feature_cols]
y = df['score']

# -------- TRAIN-TEST SPLIT -------- #
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# -------- MODEL TRAINING -------- #
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# -------- EVALUATION -------- #
y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("Model Evaluation:")
print(f" - Mean Absolute Error (MAE): {mae:.2f}")
print(f" - R² Score: {r2:.2f}")

# -------- FULL PREDICTIONS -------- #
df['ml_predicted_score'] = model.predict(X)

# -------- SAVE TO CSV -------- #
df.to_csv("wallet_scores_with_ml.csv", index=False)
print("\nSaved: wallet_scores_with_ml.csv")
print(df[['wallet', 'score', 'ml_predicted_score']].head())
