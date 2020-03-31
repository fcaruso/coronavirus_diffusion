import json
import numpy

#read data json 
def read_json_file(filename):
	f = open(filename,'r')
	return json.loads(f.read())


# create a matrix and two map: matrix, x_map and y_map
# x_map["year-month-day"] = index of the matrix column
# y_map["region-name"] = index of the matrix row
# matrix of dimension [n_regions]x[n_days][3]
# return [x_map, y_map, matrix]
def build_matrix(json_data):
	n_days = len(json_data)
	x_map = {}
	y_map = {}
	x_val = 0
	y_val = 0
	for i in range(n_days):
		item = json_data[i]
		item_date = item['data'].split("T")[0]
		item_region = item['denominazione_regione']
		if (x_map.get(item_date) == None ):
			x_map[item_date] = x_val
			x_val += 1
		if (y_map.get(item_region) == None):
			y_map[item_region] = y_val
			y_val += 1

	matrix = numpy.zeros((y_val,x_val,3))
	
	for i in range(n_days):
	    item = json_data[i]
	    item_date = item['data'].split("T")[0]
	    item_region = item['denominazione_regione']
	    index = [ y_map[item_region], x_map[item_date] ]

	    matrix[ index[0], index[1], 0] = item['tamponi']
	    matrix[ index[0], index[1], 1] = item['totale_positivi']
	    matrix[ index[0], index[1], 2] = item['nuovi_positivi']

	return [x_map,y_map,matrix]
