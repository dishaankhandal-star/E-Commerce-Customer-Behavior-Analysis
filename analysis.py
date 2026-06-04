import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sqlite3
import os

# -----------------------------
# Create output folder
# -----------------------------
os.makedirs("output", exist_ok=True)

# -----------------------------
# Load Dataset
# -----------------------------
df = pd.read_csv("data/Online Retail.csv", encoding="ISO-8859-1")

print("Dataset Loaded Successfully")
print(df.head())

# -----------------------------
# Data Cleaning
# -----------------------------
df.dropna(subset=['CustomerID'], inplace=True)

df = df[df['Quantity'] > 0]
df = df[df['UnitPrice'] > 0]

df['CustomerID'] = df['CustomerID'].astype(int)

# -----------------------------
# Create Revenue Column
# -----------------------------
df['Revenue'] = df['Quantity'] * df['UnitPrice']

# -----------------------------
# Convert Date Column
# -----------------------------
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

df['Month'] = df['InvoiceDate'].dt.to_period('M')

# -----------------------------
# Monthly Sales Analysis
# -----------------------------
monthly_sales = df.groupby('Month')['Revenue'].sum()

plt.figure(figsize=(10,5))
monthly_sales.plot()
plt.title("Monthly Revenue Trend")
plt.xlabel("Month")
plt.ylabel("Revenue")
plt.grid(True)

plt.savefig("output/monthly_sales.png")
plt.close()

# -----------------------------
# Top Products Analysis
# -----------------------------
top_products = (
    df.groupby('Description')['Revenue']
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

plt.figure(figsize=(10,5))
top_products.plot(kind='bar')

plt.title("Top 10 Products by Revenue")
plt.ylabel("Revenue")

plt.tight_layout()
plt.savefig("output/top_products.png")
plt.close()

# -----------------------------
# Country Wise Sales
# -----------------------------
country_sales = (
    df.groupby('Country')['Revenue']
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

plt.figure(figsize=(10,5))
country_sales.plot(kind='bar')

plt.title("Top Countries by Revenue")
plt.ylabel("Revenue")

plt.tight_layout()
plt.savefig("output/country_sales.png")
plt.close()

# -----------------------------
# Customer Segmentation
# -----------------------------
customer_sales = (
    df.groupby('CustomerID')['Revenue']
    .sum()
)

customer_segments = pd.DataFrame(customer_sales)

customer_segments['Segment'] = pd.qcut(
    customer_segments['Revenue'],
    q=3,
    labels=['Low Value','Medium Value','High Value']
)

customer_segments.to_csv(
    "output/customer_segments.csv"
)

# -----------------------------
# Save To SQL Database
# -----------------------------
conn = sqlite3.connect("ecommerce.db")

df.to_sql(
    "sales_data",
    conn,
    if_exists="replace",
    index=False
)

conn.close()

# -----------------------------
# Insights
# -----------------------------
print("\n----- PROJECT INSIGHTS -----")

print(
    "\nTotal Revenue:",
    round(df['Revenue'].sum(),2)
)

print(
    "\nTotal Customers:",
    df['CustomerID'].nunique()
)

print(
    "\nTop Product:"
)

print(top_products.head(1))

print(
    "\nTop Country:"
)

print(country_sales.head(1))

print("\nProject Completed Successfully")
