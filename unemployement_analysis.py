import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Set professional plot style
sns.set_style("whitegrid")
plt.rcParams.update({'font.size': 12})

#Load & Clean Data

# Load datasets
df1 = pd.read_csv("Unemployment in India.csv")
df2 = pd.read_csv("Unemployment_Rate_upto_11_2020.csv")

# Function to clean dataset
def clean_unemployment_data(df):
    df.columns = df.columns.str.strip()
    df['Date'] = pd.to_datetime(df['Date'], dayfirst=True, errors='coerce')
    df = df.dropna(subset=['Date', 'Estimated Unemployment Rate (%)'])
    return df

# Clean both datasets
df1 = clean_unemployment_data(df1)
df2 = clean_unemployment_data(df2)

# Monthly Column for Seasonality

df2['Month'] = df2['Date'].dt.month

#Plot - Unemployment Trend Over Time

plt.figure(figsize=(14, 7))
sns.lineplot(data=df2, x='Date', y='Estimated Unemployment Rate (%)', hue='Region', linewidth=2.2)
plt.axvline(pd.to_datetime("2020-03-24"), color='red', linestyle='--', label='COVID-19 Lockdown Start')
plt.title('Unemployment Rate Trends in India by Region')
plt.xlabel('Date')
plt.ylabel('Unemployment Rate (%)')
plt.xticks(rotation=45)
plt.legend(title="Region", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()

#Plot - Seasonal Pattern

monthly_avg = df2.groupby('Month')['Estimated Unemployment Rate (%)'].mean()
plt.figure(figsize=(10, 6))
sns.barplot(data=df2,x='Month',y='Estimated Unemployment Rate (%)',hue='Month',palette='crest',estimator='mean',dodge=False,legend=False)
plt.title('Average Monthly Unemployment Rate in India')
plt.xlabel('Month')
plt.ylabel('Average Unemployment Rate (%)')
plt.xticks(ticks=range(0, 12), labels=[
    "Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
])
plt.tight_layout()
plt.show()

#STEP 6: Summary Statistics

print("\n------ Dataset 1 Summary Statistics ------")
print(df1.describe())

print("\n------ Dataset 2 Summary Statistics ------")
print(df2.describe())

#Analyze COVID-19 Impact

pre_covid = df2[df2['Date'] < '2020-03-01']
post_covid = df2[df2['Date'] >= '2020-03-01']

avg_pre = pre_covid['Estimated Unemployment Rate (%)'].mean()
avg_post = post_covid['Estimated Unemployment Rate (%)'].mean()
delta = avg_post - avg_pre
print("\n------ COVID-19 IMPACT ON UNEMPLOYMENT ------")
print(f"Average Pre-COVID Unemployment Rate: {avg_pre:.2f}%")
print(f"Average Post-COVID Unemployment Rate: {avg_post:.2f}%")
print(f"Increase in Unemployment Rate Due to COVID: {delta:.2f}%")

