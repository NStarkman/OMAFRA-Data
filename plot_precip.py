import datetime
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os


# Ensure the folder "Precip Graphs" exists
if not os.path.exists('Precip Graphs'):
  os.mkdir('Precip Graphs')

# Load the CSV file into a DataFrame
df = pd.read_csv('vcr_dashboard_data.csv')

# Filter to get only the specified counties
counties = [
    "Norfolk", "Essex", "Sudbury", "Chatham-Kent", "Peterborough", "Huron",
    "Durham", "Thunder Bay", "Bruce", "Kemptville", "Lambton", "Middlesex",
    "Renfrew", "Simcoe", "Wellington Centre", "Wellington North", "Timiskaming"
]
current_year = datetime.datetime.now().year

df = df[df['County'].isin(counties)]

# Convert date column to datetime type
df['Date'] = pd.to_datetime(df['Date'])

# Extract month and year from the date column
df['Year'] = df['Date'].dt.year
df['Month'] = df['Date'].dt.month

# Find the maximum date in current year data
max_date = df[df['Year'] == current_year]['Date'].max()

# Restrict the data to current year up to the maximum date in current year data
df_curr = df[(df['Year'] == current_year) & (df['Date'] <= max_date)]

final_df = []

for county in counties:
  county_data = df[df['County'] == county]

  # Get months in current year for this county
    # Get months in current year for this county
  months_curr = df_curr[df_curr['County'] == county]['Month'].unique()

  # Calculate 10-year average for all months
  ten_years_data = county_data[(county_data['Date'].dt.year >= current_year-10) & 
                             (county_data['Date'].dt.year <= current_year-1)]
  ten_years_sums = ten_years_data.groupby(ten_years_data['Date'].dt.month
                            )['Precipitation'].sum().reset_index()
  ten_years_sums = ten_years_sums.rename(columns={'Date': 'Month'})
  ten_years_avg = ten_years_sums['Precipitation'] / 10
  
  avg_df = pd.DataFrame({
      'County': county,
      'Month': ten_years_sums['Month'],
      'Precipitation': ten_years_avg,
      'Label': '10-Year Avg'
  })

  # Only take the 10-year avg data for the months that are present in current year data for this county
  avg_df = avg_df[avg_df['Month'].isin(months_curr)]

  data_curr = df_curr[df_curr['County'] == county]
  data_curr = data_curr.groupby(['Month'])['Precipitation'].sum().reset_index()
  data_curr['Label'] = str(current_year)
  data_curr['County'] = county

  combined = pd.concat([avg_df, data_curr])
  final_df.append(combined)


final_df = pd.concat(final_df)

# Convert month numbers to names
month_mapping = {
    1: 'Jan',
    2: 'Feb',
    3: 'March',
    4: 'April',
    5: 'May',
    6: 'June',
    7: 'July',
    8: 'August',
    9: 'Sept',
    10: 'Oct',
    11: 'Nov',
    12: 'Dec'
}
final_df['Month'] = final_df['Month'].map(month_mapping)

# Plotting and saving as PNG files
for county in counties:
  county_data = final_df[final_df['County'] == county]

  # Skip plotting for counties with incomplete data
  if county_data['Label'].nunique() < 2:
    print(f"Skipping {county} due to missing data")
    continue

  plt.figure(figsize=(10, 6))
  plt.grid(axis='y', linestyle='--', linewidth=0.75, alpha=1, zorder=0)

  sns.barplot(
      x='Month',
      y='Precipitation',
      hue='Label',
      palette={
          '10-Year Avg': '#1F497D',
          str(current_year): '#00CC66'
      },
      edgecolor='black',  # This adds a black border
      linewidth=1.5,  # This specifies the thickness of the border
      width=0.5,
      data=county_data,
      hue_order=[str(current_year), '10-Year Avg'],
      zorder=2)

  plt.title(f'{county} Total Precipitation Per Month',
            fontsize=23,
            fontweight='bold')
  plt.ylabel('Precipitation (mm)', fontsize=17)
  plt.xlabel(' ')
  plt.legend(loc='upper center', fontsize=17, bbox_to_anchor=(0.5, -0.2), ncol=2)
  plt.xticks(fontsize=17)
  plt.yticks(fontsize=17)
  plt.tight_layout()  # Ensure everything fits properly
  plt.savefig(f'Precip Graphs/{county}_Precip.png')
  print(f'Finished {county} Precipitation')
  plt.close()  # Close the figure to free up memory
