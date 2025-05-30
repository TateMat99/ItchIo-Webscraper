import pandas as pd
import numpy as np

GBP_to_USD = 1.25  
EUR_to_USD = 1.10  
BRL_to_USD = 0.19  

df = pd.read_csv(os.path.join('..', 'Data', 'ScrapedInformation.csv'), sep='|')

def replace_missing_values(row):
    return row.apply(lambda x: 'none' if x == '' or pd.isnull(x) else x)

df = df.apply(replace_missing_values, axis=1)
initial_count = len(df)
df_no_duplicates = df.drop_duplicates(subset=[col for col in df.columns if col != 'scraped_id'])
df_no_duplicates = df_no_duplicates.copy()

def convert_price(price):
    price = str(price).replace(',', '')  
    price_lower = price.lower().strip()
    if price_lower == 'free' or price_lower == '$0':
        return 0.0  
    try:
        if '£' in price_lower:  
            value = float(price_lower.replace('£', '').strip())
            return value * GBP_to_USD
        elif '€' in price_lower:  
            value = float(price_lower.replace('€', '').strip())
            return value * EUR_to_USD
        elif 'r$' in price_lower:  
            value = float(price_lower.replace('r$', '').strip())
            return value * BRL_to_USD
        else:
            value = float(price_lower.replace('$', '').strip())
            return value
    except ValueError:
        return np.nan  


df_no_duplicates['price'] = df_no_duplicates['price'].apply(convert_price)
df_no_duplicates['platforms'] = df_no_duplicates['platforms'].str.split(',')
df_no_duplicates = df_no_duplicates.explode('platforms')
df_no_duplicates['platforms'] = df_no_duplicates['platforms'].str.strip()
df_no_duplicates.sort_values(by='scraped_id', inplace=True) 
df_no_duplicates.reset_index(drop=True, inplace=True) 
df_no_duplicates['scraped_id'] = range(1, len(df_no_duplicates) + 1)

final_count = len(df_no_duplicates)
duplicates_removed = initial_count - final_count

print(f"{duplicates_removed} duplicate row(s) were removed.")


df_no_duplicates.to_csv(os.path.join('..', 'Data', 'Cleaned_Data.csv'), sep='|', index=False)
