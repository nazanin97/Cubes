import pandas as pd

df = pd.read_csv('data/london12.csv', header=None)
df.columns = ['id', 'continent', 'country', 'gender', 'agegroup', 'sport', 'gold', 'silver', 'bronze']

# Question 1
top_10_contries = df.groupby('country').count()['id'].sort_values(ascending=False)[:10]
top_10_contries.plot.bar()
# Question 2
continent_medals = df.groupby('continent').sum().sum(axis=1)
continent_medals.plot.pie()

# Question 3
countries_with_more_than_30 = df.groupby('country').count()['id'].where(lambda x: x >= 30).dropna()
countries = countries_with_more_than_30.index
countries_with_more_than_30 = df[df['country'].isin(countries)]

country_medals = countries_with_more_than_30.groupby('country').sum().sum(axis=1)
country_counts = countries_with_more_than_30.groupby('country').count()['id']

top_10_medal_count_ratio = (country_medals / country_counts).sort_values(ascending=False)[:10]
top_10_medal_count_ratio.plot.bar()

