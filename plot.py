#! /usr/bin/python

from helpers import pull_data, process_data, plot_data


data = pull_data()
if not data: exit('Could not pull the data.')

try:
  processed_data = process_data(data)
except:
  exit('Could not process the data.')

try:
  plot_data(processed_data)
except:
  exit('Could not plot the data.')