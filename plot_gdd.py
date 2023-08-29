import datetime
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

# Ensure the folder "GDD Graphs" exists
if not os.path.exists('GDD Graphs'):
  os.mkdir('GDD Graphs')

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

# Extract year from the date column
df['Year'] = df['Date'].dt.year

# Find the maximum date in current year data
max_date_curr = df[df['Year'] == current_year]['Date'].max()
max_day_curr_year = max_date_curr.dayofyear

final_dfs = []

for county in counties:
  county_data = df[df['County'] == county]

  # Calculate cumulative sum for GDD for each of the last 10 years, then take the average
  ten_years_data = county_data[county_data['Year'] >= current_year-10].copy()
  ten_years_data['Cumulative_GDD'] = ten_years_data.groupby(
      'Year')['GDD'].cumsum()
  avg_cumulative_gdd = ten_years_data.groupby(
      ten_years_data['Date'].dt.dayofyear)['Cumulative_GDD'].mean(
      ).reset_index()

  avg_df = pd.DataFrame({
      'County': county,
      'DayOfYear': avg_cumulative_gdd['Date'],
      'Cumulative_GDD': avg_cumulative_gdd['Cumulative_GDD'],
      'Label': '10-Year Avg'
  })

  # Calculate cumulative sum for GDD for current year
  data_curr_year = county_data[(county_data['Year'] == current_year) & (
      county_data['Date'].dt.dayofyear <= max_day_curr_year)].copy()
  data_curr_year['Cumulative_GDD'] = data_curr_year['GDD'].cumsum()
  data_curr_year['Label'] = str(current_year)
  data_curr_year['DayOfYear'] = data_curr_year['Date'].dt.dayofyear

  combined = pd.concat(
      [avg_df, data_curr_year[['County', 'DayOfYear', 'Cumulative_GDD', 'Label']]])
  final_dfs.append(combined)

final_df = pd.concat(final_dfs)

# Set the styles directly

for county in counties:
  county_data = final_df[final_df['County'] == county]

  # Skip plotting for counties with incomplete data
  if county_data['Label'].nunique() < 2:
    print(f"Skipping {county} due to missing data")
    continue

  plt.figure(figsize=(10, 6))
  plt.grid(axis='y', linestyle='--', linewidth=0.75, alpha=1, zorder=0)

  # Plot Current Year line
  data_curr_year = county_data[county_data['Label'] == str(current_year)]
  plt.plot(
      data_curr_year['DayOfYear'],
      data_curr_year['Cumulative_GDD'],
      label=str(current_year),
      linestyle='-',  # solid line style
      linewidth=6.5,
      color='#00CC66')

  # Plot "10-Year Avg" line
  avg_data = county_data[(county_data['Label'] == '10-Year Avg')
                         & (county_data['DayOfYear'] <= max_day_curr_year)]
  plt.plot(
      avg_data['DayOfYear'],
      avg_data['Cumulative_GDD'],
      label='10-Year Avg',
      linestyle=':',  # dashed line style
      linewidth=6.5,
      color='#1F497D')

  # Customize X-axis ticks and labels
  max_labels = 25  # Maximum number of x-axis labels
  step = len(avg_data) // max_labels

  # Calculate the corresponding day of the year for x-axis labels
  label_days = avg_data['DayOfYear'][::step]

  # Create a list of datetime objects representing the days of the year
  label_dates = [
      pd.Timestamp(year=current_year, month=1, day=1) + pd.DateOffset(days=day - 1)
      for day in label_days
  ]

  # Format the dates as 'Month Day'
  label_months = [date.strftime('%b %d') for date in label_dates]

  plt.xticks(
      label_days,
      label_months,  # Use the list of formatted dates
      rotation = 90
       # Set rotation to 45 degrees
      )

  plt.title(f'{county} Growing Degree Days', fontsize=23, fontweight='bold')
  plt.ylabel('Degree Days (base 5°C)', fontsize = 17)
  plt.legend(loc='upper center', fontsize=17, bbox_to_anchor=(0.5, -0.3), ncol=2)
  plt.xticks(fontsize=17)
  plt.yticks(fontsize=17)
  plt.tight_layout()
  plt.savefig(f'GDD Graphs/{county}_GDD.png')
  print(f'Finished {county} GDD')
  plt.close()
