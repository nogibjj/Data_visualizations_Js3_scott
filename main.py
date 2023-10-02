import pandas as pd 
import geopandas as gpd
import matplotlib.pyplot as plt

def data_clean():
    df = pd.read_csv("AI_Companies.csv")
    df.drop(columns="Unnamed: 7", inplace=True)
    df.rename(columns={
        "Average Hourly Rate": "Average_Hourly_Rate",
        'Minimum Project Size': "Minimum_Project_Size",
        "Number of Employees": "Number_of_Employees",
        "Percent AI Service Focus": 'Percent_AI_Service_Focus'
    }, inplace=True)
    us_state_abbreviations = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 
                              'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 
                              'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 
                              'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 
                              'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 
                              'VA', 'WA', 'WV', 'WI', 'WY']

    # Filter rows where the 'Location' column contains state abbreviations
    df_us = df[df['Location'].str[-2:].isin(us_state_abbreviations)]
    df_us = df_us.copy()
    df_us.loc[:, 'state'] = df_us["Location"].str[-2:]



    # Define a mapping for the levels to numeric values
    mapping = {
        "Undisclosed": None,    # You can replace None with any value if needed
        "$50 - $99 / hr": 2,
        "$25 - $49 / hr": 3,
        "$100 - $149 / hr": 4,
        "< $25 / hr": 1,
        "$150 - $199 / hr": 5,
        "$200 - $300 / hr": 6,
        "$300+ / hr": 7,
    }

    # Drop the "Undisclosed" row
    df_us = df_us[df_us["Average_Hourly_Rate"] != "Undisclosed"]

    # Map the levels to numeric values
    df_us["Hourly_Rate"] = df_us["Average_Hourly_Rate"].map(mapping)
    df_final = df_us[['state','Hourly_Rate']]
    df1 = df_final.groupby('state')['Hourly_Rate'].mean().reset_index()

    # Rename the columns for clarity
    df1.columns = ['State', 'Average_Hourly_Rate']

    # Dictionary mapping state abbreviations to state names
    state_dict = {
        'AL': 'Alabama',
        'AK': 'Alaska',
        'AZ': 'Arizona',
        'AR': 'Arkansas',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'HI': 'Hawaii',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'IA': 'Iowa',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'ME': 'Maine',
        'MD': 'Maryland',
        'MA': 'Massachusetts',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MS': 'Mississippi',
        'MO': 'Missouri',
        'MT': 'Montana',
        'NE': 'Nebraska',
        'NV': 'Nevada',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NY': 'New York',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VT': 'Vermont',
        'VA': 'Virginia',
        'WA': 'Washington',
        'WV': 'West Virginia',
        'WI': 'Wisconsin',
        'WY': 'Wyoming'
    }

    # Convert state abbreviations to state names
    df1['State'] = [state_dict[abbr] for abbr in df1['State']]
    return df1


if __name__ == "__main__":

