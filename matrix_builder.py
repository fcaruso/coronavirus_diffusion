import numpy

# create a matrix and two map from dpcm-dpc json: 
# matrix, x_map and y_map
# x_map["year-month-day"] = index of the matrix column
# y_map["region-name"] = index of the matrix row
# matrix of dimension [n_regions]x[n_days][3]
# return [x_map, y_map, matrix]
def build_matrix_from_json(json_data):
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


# build a 2d matrix [n_rows]x[n_cols] given a 3d matrix [n_rows]x[n_cols][2]
# each row is the array of the ratio of [i,j,1]/[i,j,0]
# threshold is the minimum value to consider a sample
# return concentration_matrix
def build_concentration_matrix( matrix, threshold=0 ):
    [n_rows, n_cols, z] = matrix.shape
    concentration_matrix = numpy.zeros((n_rows, n_cols))
    for i in range(n_rows):
        for j in range(n_cols):
            if (( matrix[i,j,0] <= threshold ) or (matrix[i,j,1] < 0)):
                concentration_matrix[i,j] = 0
            else:
                concentration_matrix[i,j] = matrix[i,j,1] / matrix[i,j,0] * 100.
    return concentration_matrix


# return a 2d concentration matrix with the daily number of tests
# by subtracting the tests of the previous day from the total tests of the current day
def build_daily_matrix(matrix):
    [n_rows, n_cols, z] = matrix.shape
    daily_matrix = numpy.zeros((n_rows, n_cols, 2))
    daily_matrix[0,0,0] = matrix[0,0,0]
    daily_matrix[0,0,1] = matrix[0,0,2]
    for i in range(1,n_cols):
        daily_matrix[:,i,0] = matrix[:,i,0] - matrix[:,i-1,0]
        daily_matrix[:,i,1] = matrix[:,i,2]
        
    return daily_matrix

