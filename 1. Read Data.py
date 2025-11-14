#
# 1. Read Data, 2025/11/14
# File: 1. Read Data.py
# Short description of the task
#

# 1. Input
import pandas as pd

df = pd.read_excel("BBCA_Financial_Data.xlsx")

# 2. Process

# CLEAN BIG NUMBERS (76,962,905,000,000 → 76962905000000) ----
def clean_big_number(x):
    if isinstance(x, str):
        x = x.replace(",", "")  # remove thousand separator
        if x.isdigit():
            return float(x)
    return x

#CLEAN PERCENT (5.83% → 0.0583) ----
def clean_percent(x):
    if isinstance(x, str) and "%" in x:
        x = x.replace("%", "")
        return float(x) / 100
    return x

#Apply cleaning
for col in df.columns:
    df[col] = df[col].apply(clean_big_number)
    df[col] = df[col].apply(clean_percent)

#FORMAT BIG NUMBER INTO T/B/M WITH COMMA DECIMAL ----
def format_TBM(x):
    if pd.isna(x):
        return ""
    if x >= 1e12:     # Trillion
        return f"{x/1e12:.1f}".replace(".", ",") + "T"
    if x >= 1e9:      # Billion
        return f"{x/1e9:.1f}".replace(".", ",") + "B"
    if x >= 1e6:      # Million
        return f"{x/1e6:.1f}".replace(".", ",") + "M"
    return str(x)

#FORMAT PERCENTAGE AS XX,XX%
def format_percent(x):
    if pd.isna(x):
        return ""
    return f"{x*100:.2f}".replace(".", ",") + "%"

#CREATE FORMATTED OUTPUT TABLE
formatted_df = df.copy()

for col in formatted_df.columns:
    if col in ["NET_INCOME", "TOTAL_ASSETS", "STOCK_PRICE"]:  
        formatted_df[col] = formatted_df[col].apply(format_TBM)
    if col in ["NIM", "ROE", "ROA"]:
        formatted_df[col] = formatted_df[col].apply(format_percent)


# 3. Output
print("\n=== OUTPUT TABEL DENGAN FORMAT T & % ===\n")
print(formatted_df)