from requests import get
from pandas import read_csv
from io import StringIO
import matplotlib
import datetime as dt
from matplotlib import pyplot as plt
from matplotlib import dates as mdates


def pull_data():
  """
  Pulls raw data from Github.
  """

  URL = "https://raw.githubusercontent.com/owid/covid-19-data/master/public"\
    +"/data/vaccinations/vaccinations.csv"
  response = get(URL)

  return response.content.decode('utf-8') if response.ok and response.content \
    else False


def process_data(data):
  """
  Processes data and pulls out relevant values.
  """

  total_df = read_csv(StringIO(data))
  total_df = total_df[['location', 'date', 'total_vaccinations_per_hundred']]\
    .fillna(method='ffill')

  top_countries = []
  df = total_df

  while len(top_countries) < 10:
    max_total = df['total_vaccinations_per_hundred'].max()
    r = df.loc[df['total_vaccinations_per_hundred'] == max_total]
    top_countries.append(r.to_dict('records')[0])

    country = r['location'].values[0]
    df = df[df['location'] != country]

  processed_data = []
  for country in top_countries:
    country_data = {}
    loc = country['location']

    rows = total_df[total_df['location'] == loc].to_dict('records')
    country_data[loc] = [(dt.datetime.strptime(row['date'],'%Y-%m-%d').date(), \
      row['total_vaccinations_per_hundred']) for row in rows]
    
    processed_data.append(country_data)

  return processed_data


def plot_data(data):
  """
  Plots total vaccination percentage over time.
  """

  plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
  plt.gca().xaxis.set_major_locator(mdates.DayLocator())

  for datum in data:
    for country, values in datum.items():
      x = [v[0] for v in values]
      y = [v[1] for v in values]
      plt.plot(x, y, label=country)

  plt.gcf().autofmt_xdate()
  plt.xlabel('date')
  plt.ylabel('% vaccinated')
  plt.title('Top 10 countries by vaccination %')
  plt.legend()
  plt.show()