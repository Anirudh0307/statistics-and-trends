# importing Libraries
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def datafunc(filename):
    df = pd.read_csv(filename)
    yeardata = df.set_index(["Country Name", "Indicator Name"]).stack().unstack(0).reset_index()
    yeardata.columns.name = None
    return df, yeardata


file_path = 'filtered.csv'
original_df, yeardata = datafunc(file_path)

# Converting the Data to Csv
# yeardata.to_csv('filtered.csv')

countrydf = pd.read_csv('filtered.csv')
# countrydf=countrydf.dropna()'''

# 1 Descriptive statisics.
'''stat=countrydf.describe()
print(stat)'''

# 2 Correlation Heatmap
selected_data = countrydf[countrydf['Indicator Name'].isin(['Access to electricity (% of population)','Electric power consumption (kWh per capita)'])]
pivot_data = selected_data.pivot(index='Year', columns='Indicator Name', values='Pakistan')
pivot_data.dropna(inplace=True)
correlation_matrix = pivot_data.corr()
plt.figure(figsize=(8, 6))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=.5)
plt.title('Correlation Heatmap for electricity consumption and access.')
plt.show()

# 3 Line Chart For Agricultural Land

selected_data = countrydf[
    (countrydf['Indicator Name'] == 'Agricultural irrigated land (% of total agricultural land)') &
    (countrydf['Year'].notna())]  # Ensure there's a valid year

# Select only the relevant columns
selected_data = selected_data[['Year', 'Oman', 'Nepal', 'Norway']]
grouped_data = selected_data.groupby('Year').sum()
plt.figure(figsize=(10, 6))
plt.plot(grouped_data.index, grouped_data['Oman'], label='Oman')
plt.plot(grouped_data.index, grouped_data['Nepal'], label='Nepal')
plt.plot(grouped_data.index, grouped_data['Norway'], label='Norway')
plt.title('Agricultural Irrigated Land - Nepal, Oman, Norway')
plt.xlabel('Year')
plt.ylabel('Access to electricity (% of population)')
plt.legend()
plt.grid(True)
plt.show()

# 4 Boxplot For Urban Population
indicator_name = 'Urban population'
selected_data = countrydf[countrydf['Indicator Name'] == indicator_name][['Austria', 'Belgium']]
melted_data = pd.melt(selected_data, var_name='Country', value_name='Value')

# Create a boxplot
plt.figure(figsize=(10, 6))
sns.boxplot(x='Country', y='Value', data=melted_data)
plt.title(f'Boxplot for {indicator_name}')
plt.xlabel('Country')
plt.ylabel(f'{indicator_name} ')
plt.show()

# 5 Bar chart for Electricity production comparison
barchart = countrydf[countrydf[
                         'Indicator Name'] == 'Electricity production from renewable sources, excluding hydroelectric (% of total)'][
    ['New Zealand', 'South Africa']]
aggregated_data = barchart.sum()
aggregated_data.plot(kind='bar', color=['blue', 'orange', 'green', 'red'], figsize=(10, 6))
plt.title('Renewable sources electircity production - South Africa vs New Zealand.')
plt.xlabel('Country')
plt.ylabel('Electircity Production')
plt.show()

# TOP 10 VERTICAL BAR CHART
population_df = original_df[original_df['Indicator Name'] == 'Cereal yield (kg per hectare)']
population_sum = population_df.drop(['Indicator Name'], axis=1).groupby('Country Name').sum()
top_countries = population_sum.sum(axis=1).sort_values(ascending=False).head(10)
plt.figure(figsize=(10, 6))
bar_chart = sns.barplot(x=top_countries.values, y=top_countries.index, palette='magma')
plt.title('Top 10 Countries growing Cereal Yield')
plt.xlabel('Total Population')
plt.ylabel('Country')
plt.show()

# Pie Chart
filtered_df = original_df[original_df['Indicator Name'] == 'Primary completion rate, total (% of relevant age group)']
selected_columns = ['Country Name', '2020', '2021']
filtered_df = filtered_df[selected_columns]
filtered_df[['2020', '2021']] = filtered_df[['2020', '2021']].apply(pd.to_numeric, errors='coerce')
filtered_df['Sum'] = filtered_df[['2020', '2021']].sum(axis=1)
top_countries = filtered_df.sort_values(by='Sum', ascending=False).head(5)
labels = top_countries['Country Name']
sizes = top_countries['Sum']

plt.figure(figsize=(8, 8))
plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
plt.title('Top 5 Countries - Primary Completion Rate (% of relevant age group) - 2020 and 2021')
plt.show()
