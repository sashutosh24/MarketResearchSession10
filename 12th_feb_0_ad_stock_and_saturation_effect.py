# -*- coding: utf-8 -*-
"""12th feb 0- ad stock and saturation effect.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/19GEVvj3zEJdsXM3aGY8k2rdlgtUSq1B6
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Define simulation parameters
np.random.seed(42)
days = 100  # Number of days
channels = ['Channel_A', 'Channel_B', 'Channel_C']

# Generate random ad spend for each channel
ad_spend_data = {
    channel: np.random.uniform(1000, 5000, days) for channel in channels
}

df = pd.DataFrame(ad_spend_data, index=pd.date_range(start="2024-01-01", periods=days))

# Apply Ad Stock effect (carryover effect)
def ad_stock_effect(spend, decay=0.5):
    ad_stock = np.zeros_like(spend)
    ad_stock[0] = spend[0]  # First day's spend
    for t in range(1, len(spend)):
        ad_stock[t] = spend[t] + decay * ad_stock[t - 1]
    return ad_stock

# Apply Saturation effect (diminishing returns using Hill function)
def saturation_effect(ad_stock, alpha=0.0005, beta=0.7):
    return (ad_stock**beta) / (alpha + (ad_stock**beta))

# Process each channel
for channel in channels:
    df[f'{channel}_AdStock'] = ad_stock_effect(df[channel].values, decay=0.5)
    df[f'{channel}_Response'] = saturation_effect(df[f'{channel}_AdStock'])

# Visualization
plt.figure(figsize=(12, 6))

for channel in channels:
    plt.plot(df.index, df[f'{channel}_Response'], label=f'Response {channel}')

plt.xlabel("Date")
plt.ylabel("Response")
plt.title("Marketing Mix Model: Ad Stock & Saturation Effect")
plt.legend()
plt.xticks(rotation=45)
plt.grid()
plt.show()

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Define simulation parameters
np.random.seed(42)
days = 100  # Number of days
channels = ['Channel_A', 'Channel_B', 'Channel_C']

# Generate random ad spend for each channel
ad_spend_data = {
    channel: np.random.uniform(1000, 5000, days) for channel in channels
}

df = pd.DataFrame(ad_spend_data, index=pd.date_range(start="2024-01-01", periods=days))

# Function to apply Ad Stock effect (carryover effect)
def ad_stock_effect(spend, decay):
    ad_stock = np.zeros_like(spend)
    ad_stock[0] = spend[0]  # First day's spend
    for t in range(1, len(spend)):
        ad_stock[t] = spend[t] + decay * ad_stock[t - 1]
    return ad_stock

# Function to apply Saturation effect (diminishing returns using Hill function)
def saturation_effect(ad_stock, alpha, beta):
    return (ad_stock**beta) / (alpha + (ad_stock**beta))

# Different decay factors for ad stock effect
decay_values = [0.3, 0.5, 0.7]

# Different saturation parameters (α: scale factor, β: curve shape)
saturation_params = [
    (0.0005, 0.7),  # Mild saturation
    (0.0002, 0.9),  # Stronger saturation
    (0.001, 0.5)    # Weaker saturation
]

# Generate ad stock data for different decay factors
ad_stock_results = {}
for decay in decay_values:
    ad_stock_results[decay] = ad_stock_effect(df['Channel_A'].values, decay)

# Generate saturation data for different parameters
saturation_results = {}
for alpha, beta in saturation_params:
    key = f"Saturation_{alpha}_{beta}"
    saturation_results[key] = saturation_effect(ad_stock_results[0.5], alpha, beta)  # Using decay=0.5 for consistency

# Plot Ad Stock Effect with different decay values
plt.figure(figsize=(12, 5))
for decay, values in ad_stock_results.items():
    plt.plot(df.index, values, label=f'Ad Stock (Decay={decay})')

plt.xlabel("Date")
plt.ylabel("Ad Stock")
plt.title("Ad Stock Effect with Different Decay Factors")
plt.legend()
plt.xticks(rotation=45)
plt.grid()
plt.show()

# Plot Saturation Effect with different parameters
plt.figure(figsize=(12, 5))
for key, values in saturation_results.items():
    plt.plot(df.index, values, label=key)

plt.xlabel("Date")
plt.ylabel("Saturation Effect")
plt.title("Saturation Effect with Different Parameters")
plt.legend()
plt.xticks(rotation=45)
plt.grid()
plt.show()

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import shap
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# -------------------------------
# 1. Load and Prepare the Data
# -------------------------------

# Sample data based on your provided table.
data = {
    "satisfaction": ["satisfied", "satisfied", "satisfied", "satisfied", "satisfied", "satisfied", "satisfied", "satisfied"],
    "Gender": ["Female", "Male", "Female", "Female", "Female", "Male", "Female", "Male"],
    "Customer Type": ["Loyal Customer"] * 8,
    "Age": [65, 47, 15, 60, 70, 30, 66, 10],
    "Type of Travel": ["Personal Travel"] * 8,
    "Class": ["Eco", "Business", "Eco", "Eco", "Eco", "Eco", "Eco", "Eco"],
    "Flight Distance": [265, 2464, 2138, 623, 354, 1894, 227, 1812],
    "Seat comfort": [0] * 8,
    "Departure/Arrival time convenient": [0] * 8,
    "Food and drink": [0] * 8,
    "Gate location": [2, 3, 3, 3, 3, 3, 3, 3],
    "Inflight wifi service": [2, 0, 2, 3, 4, 2, 2, 2],
    "Inflight entertainment": [4, 2, 0, 4, 3, 0, 5, 0],
    "Online support": [2, 2, 2, 3, 4, 2, 5, 2],
    "Ease of Online booking": [3, 3, 2, 1, 2, 2, 5, 2],
    "On-board service": [3, 4, 3, 1, 2, 5, 0, 3],
    "Leg room service": [0, 4, 3, 0, 0, 4, 5, 3],
    "Baggage handling": [3, 4, 4, 1, 2, 5, 5, 4],
    "Checkin service": [5, 2, 4, 3, 5, 4, 5, 5],
    "Cleanliness": [3, 3, 2, 0, 0, 2, 3, 4],
    "Online boarding": [2, 2, 0, 0, 0, 0, 17, 0],
    "Departure Delay in Minutes": [0, 310, 0, 0, 0, 0, 0, 0],
    "Arrival Delay in Minutes": [0, 305, 0, 0, 0, 0, 15, 0]
}

df = pd.DataFrame(data)

# For demonstration, simulate variation in satisfaction.
# (In your real data, ensure that satisfaction has multiple values.)
df.loc[1, 'satisfaction'] = 'unsatisfied'
df.loc[4, 'satisfaction'] = 'unsatisfied'

# Convert satisfaction into a binary target variable (1 = satisfied, 0 = unsatisfied)
df['satisfaction_binary'] = df['satisfaction'].apply(lambda x: 1 if x == 'satisfied' else 0)

# -------------------------------
# 2. Feature Encoding & Splitting
# -------------------------------

# Define features (drop the original satisfaction text column)
feature_cols = df.columns.drop(['satisfaction', 'satisfaction_binary'])

# Identify categorical features (others will be treated as numeric)
categorical_features = ['Gender', 'Customer Type', 'Type of Travel', 'Class']

# One-hot encode categorical variables. (Numerical columns remain unaffected.)
df_encoded = pd.get_dummies(df[feature_cols], drop_first=True)

# Final feature matrix X and target vector y
X = df_encoded
y = df['satisfaction_binary']

# Split the dataset (for demonstration; a real dataset should be larger)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# -------------------------------
# 3. Train a Classifier
# -------------------------------

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Display basic feature importances from the model
importances = model.feature_importances_
importance_df = pd.DataFrame({'Feature': X.columns, 'Importance': importances}).sort_values(by='Importance', ascending=False)
print("Feature Importances:")
print(importance_df)

# -------------------------------
# 4. SHAP Analysis for Detailed Insights
# -------------------------------

# Initialize SHAP TreeExplainer using the trained model.
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_train)

# Plot a bar summary plot of SHAP values for the positive class (satisfied = 1)
shap.summary_plot(shap_values[1], X_train, plot_type="bar", show=False)
plt.title("SHAP Feature Importance (Bar Plot)")
plt.tight_layout()
plt.show()

# Plot a detailed SHAP summary dot plot
shap.summary_plot(shap_values[1], X_train, show=False)
plt.title("SHAP Summary Dot Plot")
plt.tight_layout()
plt.show()

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import shap
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# -------------------------------
# 1. Load and Prepare the Data
# -------------------------------

# Sample data based on your provided table.
data = {
    "satisfaction": ["satisfied", "satisfied", "satisfied", "satisfied", "satisfied", "satisfied", "satisfied", "satisfied"],
    "Gender": ["Female", "Male", "Female", "Female", "Female", "Male", "Female", "Male"],
    "Customer Type": ["Loyal Customer"] * 8,
    "Age": [65, 47, 15, 60, 70, 30, 66, 10],
    "Type of Travel": ["Personal Travel"] * 8,
    "Class": ["Eco", "Business", "Eco", "Eco", "Eco", "Eco", "Eco", "Eco"],
    "Flight Distance": [265, 2464, 2138, 623, 354, 1894, 227, 1812],
    "Seat comfort": [0] * 8,
    "Departure/Arrival time convenient": [0] * 8,
    "Food and drink": [0] * 8,
    "Gate location": [2, 3, 3, 3, 3, 3, 3, 3],
    "Inflight wifi service": [2, 0, 2, 3, 4, 2, 2, 2],
    "Inflight entertainment": [4, 2, 0, 4, 3, 0, 5, 0],
    "Online support": [2, 2, 2, 3, 4, 2, 5, 2],
    "Ease of Online booking": [3, 3, 2, 1, 2, 2, 5, 2],
    "On-board service": [3, 4, 3, 1, 2, 5, 0, 3],
    "Leg room service": [0, 4, 3, 0, 0, 4, 5, 3],
    "Baggage handling": [3, 4, 4, 1, 2, 5, 5, 4],
    "Checkin service": [5, 2, 4, 3, 5, 4, 5, 5],
    "Cleanliness": [3, 3, 2, 0, 0, 2, 3, 4],
    "Online boarding": [2, 2, 0, 0, 0, 0, 17, 0],
    "Departure Delay in Minutes": [0, 310, 0, 0, 0, 0, 0, 0],
    "Arrival Delay in Minutes": [0, 305, 0, 0, 0, 0, 15, 0]
}

df = pd.DataFrame(data)

# For demonstration, simulate variation in satisfaction.
# (In your real data, ensure that satisfaction has multiple values.)
df.loc[1, 'satisfaction'] = 'unsatisfied'
df.loc[4, 'satisfaction'] = 'unsatisfied'

# Convert satisfaction into a binary target variable (1 = satisfied, 0 = unsatisfied)
df['satisfaction_binary'] = df['satisfaction'].apply(lambda x: 1 if x == 'satisfied' else 0)

# -------------------------------
# 2. Feature Encoding & Splitting
# -------------------------------

# Define features (drop the original satisfaction text column)
feature_cols = df.columns.drop(['satisfaction', 'satisfaction_binary'])

# Identify categorical features (others will be treated as numeric)
categorical_features = ['Gender', 'Customer Type', 'Type of Travel', 'Class']

# One-hot encode categorical variables. (Numerical columns remain unaffected.)
df_encoded = pd.get_dummies(df[feature_cols], drop_first=True)

# Final feature matrix X and target vector y
X = df_encoded
y = df['satisfaction_binary']

# Split the dataset (for demonstration; a real dataset should be larger)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# -------------------------------
# 3. Train a Classifier
# -------------------------------

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Display basic feature importances from the model
importances = model.feature_importances_
importance_df = pd.DataFrame({'Feature': X.columns, 'Importance': importances}).sort_values(by='Importance', ascending=False)
print("Feature Importances:")
print(importance_df)

# -------------------------------
# 4. SHAP Analysis for Detailed Insights
# -------------------------------

# Initialize SHAP TreeExplainer using the trained model.
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_train)

# Plot a bar summary plot of SHAP values for the positive class (satisfied = 1)
shap.summary_plot(shap_values[1], X_train, plot_type="bar", show=False)
plt.title("SHAP Feature Importance (Bar Plot)")
plt.tight_layout()
plt.show()

# Plot a detailed SHAP summary dot plot
shap.summary_plot(shap_values[1], X_train, show=False)
plt.title("SHAP Summary Dot Plot")
plt.tight_layout()
plt.show()

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import shap
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

# -------------------------------
# 1. Read Excel Data
# -------------------------------
excel_path = '/content/Invistico_Airline.csv'  # Replace with your Excel file path
df = pd.read_excel(excel_path)

# -------------------------------
# 2. Data Preparation
# -------------------------------
# Inspect the first few rows (optional)
print("Data Preview:")
print(df.head())

# If the 'satisfaction' column has only one unique value,
# simulate some unsatisfied responses for demonstration.
if df['satisfaction'].nunique() == 1:
    df.loc[df.index[1], 'satisfaction'] = 'unsatisfied'
    df.loc[df.index[4], 'satisfaction'] = 'unsatisfied'

# Convert satisfaction to a binary target (1 = satisfied, 0 = unsatisfied)
df['satisfaction_binary'] = df['satisfaction'].apply(lambda x: 1 if x == 'satisfied' else 0)

# Define features by dropping the original satisfaction labels
feature_cols = [col for col in df.columns if col not in ['satisfaction', 'satisfaction_binary']]

# Identify categorical variables that need one-hot encoding
categorical_features = ['Gender', 'Customer Type', 'Type of Travel', 'Class']

# One-hot encode categorical features; numeric columns remain unchanged.
df_encoded = pd.get_dummies(df[feature_cols], columns=categorical_features, drop_first=True)

# Define feature matrix X and target vector y
X = df_encoded
y = df['satisfaction_binary']

# -------------------------------
# 3. Train-Test Split & Logistic Regression
# -------------------------------
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Train a Logistic Regression model
model = LogisticRegression(random_state=42, solver='liblinear')
model.fit(X_train, y_train)

# Optional: Print model coefficients for a quick look at feature effects
coefficients = pd.DataFrame({
    'Feature': X_train.columns,
    'Coefficient': model.coef_[0]
}).sort_values(by='Coefficient', ascending=False)
print("Logistic Regression Coefficients:")
print(coefficients)

# -------------------------------
# 4. SHAP Analysis & Visualization
# -------------------------------
# Initialize SHAP LinearExplainer for the logistic regression model
explainer = shap.LinearExplainer(model, X_train, feature_dependence="independent")
shap_values = explainer.shap_values(X_train)

# SHAP Bar Plot: Displays average absolute SHAP values by feature importance
shap.summary_plot(shap_values, X_train, plot_type="bar", show=False)
plt.title("SHAP Feature Importance (Bar Plot)")
plt.tight_layout()
plt.show()

# SHAP Dot Plot: Detailed summary showing feature impacts across samples
shap.summary_plot(shap_values, X_train, show=False)
plt.title("SHAP Summary Dot Plot")
plt.tight_layout()
plt.show()

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import shap
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

# -------------------------------
# 1. Read CSV Data
# -------------------------------
csv_path = '/content/Invistico_Airline.csv'  # CSV file path
df = pd.read_csv(csv_path)

# -------------------------------
# 2. Data Preparation
# -------------------------------
# Optional: Inspect the first few rows
print("Data Preview:")
print(df.head())

# For demonstration, if the dataset only contains "satisfied" values,
# simulate some unsatisfied responses (ensure you have variation in real data).
if df['satisfaction'].nunique() == 1:
    df.loc[df.index[1], 'satisfaction'] = 'unsatisfied'
    df.loc[df.index[4], 'satisfaction'] = 'unsatisfied'

# Convert satisfaction to a binary target variable: 1 = satisfied, 0 = unsatisfied
df['satisfaction_binary'] = df['satisfaction'].apply(lambda x: 1 if x == 'satisfied' else 0)

# Define feature columns (dropping satisfaction labels)
feature_cols = [col for col in df.columns if col not in ['satisfaction', 'satisfaction_binary']]

# Identify categorical features to encode; adjust these based on your actual data columns.
categorical_features = ['Gender', 'Customer Type', 'Type of Travel', 'Class']

# One-hot encode categorical features (numeric columns remain unchanged)
df_encoded = pd.get_dummies(df[feature_cols], columns=categorical_features, drop_first=True)

# Final feature matrix and target vector
X = df_encoded
y = df['satisfaction_binary']

# -------------------------------
# 3. Train-Test Split & Logistic Regression
# -------------------------------
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Train a Logistic Regression model
model = LogisticRegression(random_state=42, solver='liblinear')
model.fit(X_train, y_train)

# Optional: Display model coefficients for insight into feature effects
coefficients = pd.DataFrame({
    'Feature': X_train.columns,
    'Coefficient': model.coef_[0]
}).sort_values(by='Coefficient', ascending=False)
print("Logistic Regression Coefficients:")
print(coefficients)

# -------------------------------
# 4. SHAP Analysis & Visualization
# -------------------------------
# Initialize SHAP LinearExplainer for the logistic regression model
explainer = shap.LinearExplainer(model, X_train, feature_dependence="independent")
shap_values = explainer.shap_values(X_train)

# SHAP Bar Plot: Rank features by their average impact on the model output
shap.summary_plot(shap_values, X_train, plot_type="bar", show=False)
plt.title("SHAP Feature Importance (Bar Plot)")
plt.tight_layout()
plt.show()

# SHAP Dot Plot: Detailed summary showing individual feature contributions
shap.summary_plot(shap_values, X_train, show=False)
plt.title("SHAP Summary Dot Plot")
plt.tight_layout()
plt.show()

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import shap
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer

# -------------------------------
# 1. Read CSV Data
# -------------------------------
csv_path = '/content/Invistico_Airline.csv'  # Your CSV file path
df = pd.read_csv(csv_path)

# -------------------------------
# 2. Data Preparation
# -------------------------------
# Preview the data
print("Data Preview:")
print(df.head())

# (Optional) Simulate unsatisfied responses if necessary for variation
if df['satisfaction'].nunique() == 1:
    df.loc[df.index[1], 'satisfaction'] = 'unsatisfied'
    df.loc[df.index[4], 'satisfaction'] = 'unsatisfied'

# Convert satisfaction to binary (1 = satisfied, 0 = unsatisfied)
df['satisfaction_binary'] = df['satisfaction'].apply(lambda x: 1 if x == 'satisfied' else 0)

# Define feature columns (exclude satisfaction labels)
feature_cols = [col for col in df.columns if col not in ['satisfaction', 'satisfaction_binary']]

# Specify categorical features to be one-hot encoded (adjust these names if needed)
categorical_features = ['Gender', 'Customer Type', 'Type of Travel', 'Class']

# One-hot encode categorical features (numeric columns remain unchanged)
df_encoded = pd.get_dummies(df[feature_cols], columns=categorical_features, drop_first=True)

# Final feature matrix X and target vector y
X = df_encoded
y = df['satisfaction_binary']

# -------------------------------
# 3. Train-Test Split & Missing Value Imputation
# -------------------------------
# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Impute missing values (if any) using the mean strategy
imputer = SimpleImputer(strategy='mean')
X_train_imputed = pd.DataFrame(imputer.fit_transform(X_train),
                               columns=X_train.columns, index=X_train.index)
X_test_imputed = pd.DataFrame(imputer.transform(X_test),
                              columns=X_test.columns, index=X_test.index)

# -------------------------------
# 4. Train Logistic Regression Model
# -------------------------------
model = LogisticRegression(random_state=42, solver='liblinear')
model.fit(X_train_imputed, y_train)

# Display model coefficients for insight into feature effects
coefficients = pd.DataFrame({
    'Feature': X_train_imputed.columns,
    'Coefficient': model.coef_[0]
}).sort_values(by='Coefficient', ascending=False)
print("Logistic Regression Coefficients:")
print(coefficients)

# -------------------------------
# 5. SHAP Analysis & Visualization
# -------------------------------
# Initialize SHAP LinearExplainer for the logistic regression model
explainer = shap.LinearExplainer(model, X_train_imputed, feature_dependence="independent")
shap_values = explainer.shap_values(X_train_imputed)

# SHAP Bar Plot: Rank features by average impact
shap.summary_plot(shap_values, X_train_imputed, plot_type="bar", show=False)
plt.title("SHAP Feature Importance (Bar Plot)")
plt.tight_layout()
plt.show()

# SHAP Summary Dot Plot: Detailed overview of feature impacts
shap.summary_plot(shap_values, X_train_imputed, show=False)
plt.title("SHAP Summary Dot Plot")
plt.tight_layout()
plt.show()

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import shap
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer

# -------------------------------
# 1. Read CSV Data
# -------------------------------
csv_path = '/content/Invistico_Airline.csv'  # Your CSV file path
df = pd.read_csv(csv_path)

# -------------------------------
# 2. Data Preparation
# -------------------------------
# Preview the data
print("Data Preview:")
print(df.head())

# (Optional) Simulate unsatisfied responses if necessary for variation
if df['satisfaction'].nunique() == 1:
    df.loc[df.index[1], 'satisfaction'] = 'unsatisfied'
    df.loc[df.index[4], 'satisfaction'] = 'unsatisfied'

# Convert satisfaction to binary (1 = satisfied, 0 = unsatisfied)
df['satisfaction_binary'] = df['satisfaction'].apply(lambda x: 1 if x == 'satisfied' else 0)

# Define feature columns (exclude satisfaction labels)
feature_cols = [col for col in df.columns if col not in ['satisfaction', 'satisfaction_binary']]

# Specify categorical features to be one-hot encoded (adjust names as needed)
categorical_features = ['Gender', 'Customer Type', 'Type of Travel', 'Class']

# One-hot encode categorical features; numeric columns remain unchanged.
df_encoded = pd.get_dummies(df[feature_cols], columns=categorical_features, drop_first=True)

# Final feature matrix X and target vector y
X = df_encoded
y = df['satisfaction_binary']

# -------------------------------
# 3. Train-Test Split & Missing Value Imputation
# -------------------------------
# Split the data into training and testing sets.
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Impute missing values (if any) using the mean strategy.
imputer = SimpleImputer(strategy='mean')
X_train_imputed = pd.DataFrame(imputer.fit_transform(X_train),
                               columns=X_train.columns, index=X_train.index)
X_test_imputed = pd.DataFrame(imputer.transform(X_test),
                              columns=X_test.columns, index=X_test.index)

# -------------------------------
# 4. Train Logistic Regression Model
# -------------------------------
model = LogisticRegression(random_state=42, solver='liblinear')
model.fit(X_train_imputed, y_train)

# Optional: Display model coefficients for insight into feature effects.
coefficients = pd.DataFrame({
    'Feature': X_train_imputed.columns,
    'Coefficient': model.coef_[0]
}).sort_values(by='Coefficient', ascending=False)
print("Logistic Regression Coefficients:")
print(coefficients)

# -------------------------------
# 5. SHAP Analysis & Visualization
# -------------------------------
# Initialize SHAP LinearExplainer for the logistic regression model,
# using 'feature_perturbation' instead of the deprecated 'feature_dependence'.
explainer = shap.LinearExplainer(model, X_train_imputed, feature_perturbation="independent")
shap_values = explainer.shap_values(X_train_imputed)

# SHAP Bar Plot: Rank features by their average impact.
shap.summary_plot(shap_values, X_train_imputed, plot_type="bar", show=False)
plt.title("SHAP Feature Importance (Bar Plot)")
plt.tight_layout()
plt.show()

# SHAP Dot Plot: Detailed overview of feature contributions.
shap.summary_plot(shap_values, X_train_imputed, show=False)
plt.title("SHAP Summary Dot Plot")
plt.tight_layout()
plt.show()

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import shap
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer

# -------------------------------
# 1. Read CSV Data
# -------------------------------
csv_path = '/content/Invistico_Airline.csv'  # Your CSV file path
df = pd.read_csv(csv_path)

# -------------------------------
# 2. Data Preparation
# -------------------------------
# Preview the data
print("Data Preview:")
print(df.head())

# (Optional) Simulate unsatisfied responses if necessary for variation
if df['satisfaction'].nunique() == 1:
    df.loc[df.index[1], 'satisfaction'] = 'unsatisfied'
    df.loc[df.index[4], 'satisfaction'] = 'unsatisfied'

# Convert satisfaction to binary (1 = satisfied, 0 = unsatisfied)
df['satisfaction_binary'] = df['satisfaction'].apply(lambda x: 1 if x == 'satisfied' else 0)

# Define feature columns (exclude satisfaction labels)
feature_cols = [col for col in df.columns if col not in ['satisfaction', 'satisfaction_binary']]

# Specify categorical features to be one-hot encoded (adjust names as needed)
categorical_features = ['Gender', 'Customer Type', 'Type of Travel', 'Class']

# One-hot encode categorical features; numeric columns remain unchanged.
df_encoded = pd.get_dummies(df[feature_cols], columns=categorical_features, drop_first=True)

# Final feature matrix X and target vector y
X = df_encoded
y = df['satisfaction_binary']

# -------------------------------
# 3. Train-Test Split & Missing Value Imputation
# -------------------------------
# Split the data into training and testing sets.
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Impute missing values (if any) using the mean strategy.
imputer = SimpleImputer(strategy='mean')
X_train_imputed = pd.DataFrame(imputer.fit_transform(X_train),
                               columns=X_train.columns, index=X_train.index)
X_test_imputed = pd.DataFrame(imputer.transform(X_test),
                              columns=X_test.columns, index=X_test.index)

# -------------------------------
# 4. Train Logistic Regression Model
# -------------------------------
model = LogisticRegression(random_state=42, solver='liblinear')
model.fit(X_train_imputed, y_train)

# Optional: Display model coefficients for insight into feature effects.
coefficients = pd.DataFrame({
    'Feature': X_train_imputed.columns,
    'Coefficient': model.coef_[0]
}).sort_values(by='Coefficient', ascending=False)
print("Logistic Regression Coefficients:")
print(coefficients)

# -------------------------------
# 5. SHAP Analysis & Visualization
# -------------------------------
# Initialize SHAP LinearExplainer for the logistic regression model,
# using 'interventional' as the allowed value for feature_perturbation.
explainer = shap.LinearExplainer(model, X_train_imputed, feature_perturbation="interventional")
shap_values = explainer.shap_values(X_train_imputed)

# SHAP Bar Plot: Rank features by their average impact.
shap.summary_plot(shap_values, X_train_imputed, plot_type="bar", show=False)
plt.title("SHAP Feature Importance (Bar Plot)")
plt.tight_layout()
plt.show()

# SHAP Summary Dot Plot: Detailed overview of feature contributions.
shap.summary_plot(shap_values, X_train_imputed, show=False)
plt.title("SHAP Summary Dot Plot")
plt.tight_layout()
plt.show()

import numpy as np
import random
import matplotlib.pyplot as plt

# Define the environment parameters
num_states = 5  # Simulated demand levels (Very Low to Very High)
num_actions = 3  # Pricing strategies (Low, Medium, High)

# Initialize the Q-table with zeros
Q_table = np.zeros((num_states, num_actions))

# Define learning parameters
alpha = 0.1  # Learning rate
gamma = 0.9  # Discount factor
epsilon = 1.0  # Exploration-exploitation tradeoff
epsilon_decay = 0.995  # Decay rate for epsilon
min_epsilon = 0.01  # Minimum exploration probability
num_episodes = 1000  # Total training episodes

# Simulated reward function for dynamic pricing
def get_reward(state, action):
    """Defines a reward based on the demand level and pricing strategy."""
    if state == 0:  # Very Low Demand
        return -5 if action == 2 else (2 if action == 0 else -1)
    elif state == 1:  # Low Demand
        return -3 if action == 2 else (5 if action == 0 else 2)
    elif state == 2:  # Medium Demand
        return 3 if action == 1 else (1 if action == 0 else 5)
    elif state == 3:  # High Demand
        return 6 if action == 2 else (4 if action == 1 else -2)
    elif state == 4:  # Very High Demand
        return 8 if action == 2 else (5 if action == 1 else -3)

# Store total rewards per episode for visualization
episode_rewards = []

# Q-Learning algorithm
for episode in range(num_episodes):
    state = random.randint(0, num_states - 1)  # Start in a random state
    total_reward = 0

    for _ in range(10):  # Limit steps per episode
        if random.uniform(0, 1) < epsilon:
            action = random.randint(0, num_actions - 1)  # Explore
        else:
            action = np.argmax(Q_table[state, :])  # Exploit best known action

        reward = get_reward(state, action)
        next_state = random.randint(0, num_states - 1)  # Simulated transition to a new state

        # Update Q-value using Bellman Equation
        Q_table[state, action] = Q_table[state, action] + alpha * (
            reward + gamma * np.max(Q_table[next_state, :]) - Q_table[state, action]
        )

        state = next_state  # Move to next state
        total_reward += reward

    episode_rewards.append(total_reward)  # Track total reward per episode

    # Reduce epsilon (exploration rate)
    epsilon = max(min_epsilon, epsilon * epsilon_decay)

# Plot the learning curve
plt.figure(figsize=(10, 5))
plt.plot(episode_rewards, label="Total Reward per Episode", color="blue")
plt.xlabel("Episodes")
plt.ylabel("Total Reward")
plt.title("Q-Learning Convergence: Search Pricing Reinforcement Learning")
plt.legend()
plt.show()

import numpy as np
import random
import matplotlib.pyplot as plt
import seaborn as sns

# Define the environment parameters
num_states = 5  # Simulated demand levels (Very Low to Very High)
num_actions = 3  # Pricing strategies (Low, Medium, High)

# Initialize the Q-table with zeros
Q_table = np.zeros((num_states, num_actions))

# Define learning parameters
alpha = 0.1  # Learning rate
gamma = 0.9  # Discount factor
epsilon = 1.0  # Exploration-exploitation tradeoff
epsilon_decay = 0.995  # Decay rate for epsilon
min_epsilon = 0.01  # Minimum exploration probability
num_episodes = 300  # Reduced training episodes for better visualization

# Simulated reward function for dynamic pricing
def get_reward(state, action):
    """Defines a reward based on the demand level and pricing strategy."""
    reward_matrix = [
        [-5, -1, 2],   # Very Low Demand
        [-3, 2, 5],    # Low Demand
        [1, 3, 5],     # Medium Demand
        [-2, 4, 6],    # High Demand
        [-3, 5, 8]     # Very High Demand
    ]
    return reward_matrix[state][action]

# Store total rewards per episode for visualization
episode_rewards = []

# Q-Learning algorithm
for episode in range(num_episodes):
    state = random.randint(0, num_states - 1)  # Start in a random state
    total_reward = 0

    for _ in range(10):  # Limit steps per episode
        if random.uniform(0, 1) < epsilon:
            action = random.randint(0, num_actions - 1)  # Explore
        else:
            action = np.argmax(Q_table[state, :])  # Exploit best known action

        reward = get_reward(state, action)
        next_state = random.randint(0, num_states - 1)  # Simulated transition to a new state

        # Update Q-value using Bellman Equation
        Q_table[state, action] = Q_table[state, action] + alpha * (
            reward + gamma * np.max(Q_table[next_state, :]) - Q_table[state, action]
        )

        state = next_state  # Move to next state
        total_reward += reward

    episode_rewards.append(total_reward)  # Track total reward per episode

    # Reduce epsilon (exploration rate)
    epsilon = max(min_epsilon, epsilon * epsilon_decay)

# Improved visualization
plt.figure(figsize=(12, 6))
sns.lineplot(x=range(num_episodes), y=episode_rewards, label="Total Reward per Episode", color="blue")
plt.xlabel("Episodes")
plt.ylabel("Total Reward")
plt.title("Q-Learning Convergence: Search Pricing Reinforcement Learning")
plt.legend()
plt.grid(True)
plt.show()

# Heatmap of final Q-table
plt.figure(figsize=(8, 6))
sns.heatmap(Q_table, annot=True, cmap="coolwarm", xticklabels=["Low", "Medium", "High"], yticklabels=["Very Low", "Low", "Medium", "High", "Very High"])
plt.xlabel("Pricing Strategy")
plt.ylabel("Demand Level")
plt.title("Final Q-Table Heatmap")
plt.show()