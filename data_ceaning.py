import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from datetime import datetime

df = pd.read_csv('W33836_business_analytics.csv')

# Drop columns
# This are the columns we considered unnecxesary due to lack of data or relevance
df = df.drop('ID', axis=1)
df = df.drop('Complain', axis=1)
df = df.drop('Z_CostContact', axis=1)
df = df.drop('Z_Revenue', axis=1)
df = df.drop('Response', axis=1)

# Remove rows where Marital_Status is 'YOLO'
# There were two persons with a maratial status names YOLO and we decided to remove it
df = df[df['Marital_Status'] != 'YOLO']

# Transform Dt_Costumer to Szn_Costumer (Spring=1, Summer=2, Fall=3, Winter=4)
# We originally thought it was a good idea to analyze the dates in shape of seazons instead of
# exact dates so we mande a function to transform that data.
# We didn't use seasons at the end so this function is not used.
def get_season(date_str):
    for fmt in ('%d/%m/%y', '%d-%m-%Y', '%d/%m/%Y'):
        try:
            dt = datetime.strptime(str(date_str), fmt)
            break
        except Exception:
            continue
    else:
        return None
    month = dt.month
    if month in [3, 4, 5]:
        return 1  # Spring
    elif month in [6, 7, 8]:
        return 2  # Summer
    elif month in [9, 10, 11]:
        return 3  # Fall
    else:
        return 4  # Winter


# Calculate customer age based on birth year and Dt_Customer, then replace birth year with age
# We thought dealing with ages was better than dealing with year births so we changed that
# relative to the date that the person shopped
if 'Year_Birth' in df.columns and 'Dt_Customer' in df.columns:
    def calculate_age(birth_year, date_str):
        # Try multiple date formats
        for fmt in ('%d/%m/%y', '%d-%m-%Y', '%d/%m/%Y', '%Y-%m-%d'):
            try:
                dt = datetime.strptime(str(date_str), fmt)
                break
            except Exception:
                continue
        else:
            return None
        try:
            age = dt.year - int(birth_year)
            return age
        except Exception:
            return None
    df['Year_Birth'] = df.apply(lambda row: calculate_age(row['Year_Birth'], row['Dt_Customer']), axis=1)

# Transform Dt_Customer to season number
# This is the funtion we didn't use
# df['Dt_Customer'] = df['Dt_Customer'].apply(get_season)


# Fill missing income values
# Replace empty strings and whitespace with NaN in 'Income'
df['Income'] = df['Income'].replace(r'^\s*$', None, regex=True)
df['Income'] = pd.to_numeric(df['Income'], errors='coerce')
mean_income = df['Income'].mean()
df['Income'] = df['Income'].fillna(mean_income)
# Round all income values to the nearest whole number and convert to int
# (drop decimals)
df['Income'] = df['Income'].round(0).astype('Int64')


# Transform education
education_map = {
    'Graduation': 1,
    'Master': 2,
    'PhD': 3,
    '2n Cycle': 4,
}
df['Education'] = df['Education'].map(education_map).fillna(0).astype(int)


# Transform maratial status
marital_status_map = {
    'Single': 1,
    'Married': 2,
    'Together': 3,
    'Divorced': 4,
    'Widow': 5
}

df['Marital_Status'] = df['Marital_Status'].map(marital_status_map).fillna(0).astype(int)


# Standardize all Dt_Customer dates to 00/00/0000 format
def standardize_date(date_str):
    # Try multiple date formats
    for fmt in ('%d/%m/%y', '%d-%m-%Y', '%d/%m/%Y', '%Y-%m-%d'):
        try:
            dt = datetime.strptime(str(date_str), fmt)
            return dt.strftime('%d/%m/%Y')
        except Exception:
            continue
    return date_str

if 'Dt_Customer' in df.columns:
    df['Dt_Customer'] = df['Dt_Customer'].apply(standardize_date)

# Save cleaned data for next steps
df.to_csv('cleaned_and_transformed_data.csv', index=False)