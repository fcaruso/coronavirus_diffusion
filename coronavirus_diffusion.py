import json
import chart_plotter as cp
import matrix_builder as mb
import numpy
from matplotlib import dates
from matplotlib.dates import DayLocator, HourLocator, DateFormatter, drange

#read data json 
json_filename = "../../COVID-19/dati-json/dpc-covid19-ita-regioni.json"
f = open(json_filename,'r')
json_data =  json.loads(f.read())

# get the essential data structures
[indexmap_date, indexmap_region, matrix] = mb.build_matrix_from_json(json_data)

concentration_matrix = mb.build_concentration_matrix(matrix, 60)
daily_matrix = mb.build_daily_matrix(matrix)
daily_concentration_matrix = mb.build_concentration_matrix(daily_matrix, 20)

list_regions = list(indexmap_region.keys())
list_dates = dates.datestr2num([ d for d in indexmap_date.keys()])
array_sum_of_concentrations = mb.build_sum_of_concentration_array(concentration_matrix)
array_sum_of_swabs = mb.build_sum_of_swabs_array(matrix)
array_sum_of_positives = mb.build_sum_of_positives_array(matrix)
sorted_average_map = mb.build_regional_averages_map(list_regions, concentration_matrix)
cp.plot_regional_charts( list_dates, list_regions, matrix, concentration_matrix,"../img/","regionale") 
cp.plot_national_charts( list_dates, array_sum_of_concentrations, array_sum_of_swabs, array_sum_of_positives,"../img/","nazionale") 
cp.plot_regional_daily_charts(list_dates, list_regions, daily_matrix, daily_concentration_matrix,"../img/", "daily")
cp.plot_regional_averages( sorted_average_map, "../img/", "regional_averages")