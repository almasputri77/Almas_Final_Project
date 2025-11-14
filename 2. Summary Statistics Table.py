#
# 2. Summary Statictics Table, 2025/11/14
# File: 2. Summary Statictics Table.py
# Short description of the task
#

# 1. Input
import pandas as pd
import numpy as np

# 2. Process
df = pd.read_excel("BBCA_Financial_Data.xlsx")

# --- Helper Functions ---

# Convert large numbers to trillion format (T)
def format_trillion(x):
    if pd.isna(x):
        return x
    if abs(x) >= 1e12:
        return f"{x/1e12:.1f}T"
    return f"{x:,.1f}"

# Convert decimals to percent format (5.80%)
def format_percent(x):
    if pd.isna(x):
        return x
    return f"{x*100:.2f}%"


# Process: Compute Summary Statistics
def summary_statistics(df):
    summary = pd.DataFrame()
    summary["N"] = df.count()
    summary["Mean"] = df.mean(numeric_only=True)
    summary["Std Dev"] = df.std(numeric_only=True)
    summary["Min"] = df.min(numeric_only=True)
    summary["Max"] = df.max(numeric_only=True)
    summary["Missing"] = df.isna().sum()
    summary["Outliers"] = df.apply(
        lambda x: ((x < (x.mean() - 3*x.std())) | (x > (x.mean() + 3*x.std()))).sum()
    )
    return summary

summary_table = summary_statistics(df)

# Exclude YEAR from numeric summary
numeric_df = df.drop(columns=["YEAR"], errors="ignore")

summary_table = summary_statistics(numeric_df)

# Output Formatting
formatted = summary_table.copy()

for col in ["Mean", "Std Dev", "Min", "Max"]:
    formatted[col] = formatted[col].apply(format_trillion)

# Detect percent variables by name
percent_vars = ["NIM", "ROE", "ROA"]

for var in percent_vars:
    if var in formatted.index:
        for col in ["Mean", "Std Dev", "Min", "Max"]:
            # Format percent values
            formatted.loc[var, col] = format_percent(summary_table.loc[var, col])

# 3. Output
print("\nSummary Statistics Table:\n")
print(formatted)