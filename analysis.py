import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sqlite3
import os

# Create Output Folder

os.makedirs("output", exist_ok=True)


# Load Dataset


print("Loading Dataset...")

df = pd.read_excel(
    "data/online_retail_II.xlsx",
    sheet_name="Year 2010-2011"
)

print("Dataset Loaded Successfully")


# Basic Information


print("\nDataset Shape:")
print(df.shape)

print("\nColumns:")
print(df.columns.tolist())


# Data Cleaning


print("\nCleaning Data...")

df.dropna(subset=["Customer ID"], inplace=True)

df = df[df["Quantity"] > 0]
df = df[df["Price"] > 0]

df["Customer ID"] = df["Customer ID"].astype(int)

# Revenue Calculation


df["Revenue"] = df["Quantity"] * df["Price"]


# Date Processing


df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

df["Month"] = df["InvoiceDate"].dt.to_period("M")

# Monthly Revenue Analysis


monthly_sales = df.groupby("Month")["Revenue"].sum()

plt.figure(figsize=(12,6))
monthly_sales.plot()

plt.title("Monthly Revenue Trend")
plt.xlabel("Month")
plt.ylabel("Revenue")
plt.grid(True)

plt.tight_layout()
plt.savefig("output/monthly_sales.png")
plt.close()

print("Monthly Revenue Graph Saved")


# Top 10 Products


top_products = (
    df.groupby("Description")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

plt.figure(figsize=(12,6))
top_products.plot(kind="bar")

plt.title("Top 10 Products by Revenue")
plt.ylabel("Revenue")

plt.tight_layout()
plt.savefig("output/top_products.png")
plt.close()

print("Top Products Graph Saved")


# Country Wise Revenue


country_sales = (
    df.groupby("Country")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

plt.figure(figsize=(12,6))
country_sales.plot(kind="bar")

plt.title("Top Countries by Revenue")
plt.ylabel("Revenue")

plt.tight_layout()
plt.savefig("output/country_sales.png")
plt.close()

print("Country Revenue Graph Saved")


# Customer Segmentation

customer_sales = (
    df.groupby("Customer ID")["Revenue"]
    .sum()
)

customer_segments = pd.DataFrame(customer_sales)

customer_segments["Segment"] = pd.qcut(
    customer_segments["Revenue"],
    q=3,
    labels=["Low Value", "Medium Value", "High Value"]
)

customer_segments.to_csv(
    "output/customer_segments.csv"
)

print("Customer Segmentation File Saved")


# Store Data in SQL Database


conn = sqlite3.connect("ecommerce.db")

df.to_sql(
    "sales_data",
    conn,
    if_exists="replace",
    index=False
)

conn.close()

print("Database Created Successfully")

# Final Insights


print("\n========== PROJECT INSIGHTS ==========")

print(
    "\nTotal Revenue Generated:",
    round(df["Revenue"].sum(), 2)
)

print(
    "\nTotal Customers:",
    df["Customer ID"].nunique()
)

print(
    "\nTotal Products:",
    df["Description"].nunique()
)

print("\nTop Product By Revenue:")
print(top_products.head(1))

print("\nTop Country By Revenue:")
print(country_sales.head(1))

print("\nProject Completed Successfully!")
