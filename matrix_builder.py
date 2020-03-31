import numpy

# build a 2d matrix [n_rows]x[n_cols] given a 3d matrix [n_rows]x[n_cols][2]
# each row is the array of the ratio of [i,j,1]/[i,j,0]
# threshold is the minimum value to consider a sample 
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


# return a matrix with the daily number of tests
# by subtracting the tests of the previous day
def build_daily_matrix(matrix):
    [n_rows, n_cols, z] = matrix.shape
    daily_matrix = numpy.zeros((n_rows, n_cols, 2))
    daily_matrix[0,0,0] = matrix[0,0,0]
    daily_matrix[0,0,1] = matrix[0,0,2]
    for i in range(1,n_cols):
        daily_matrix[:,i,0] = matrix[:,i,0] - matrix[:,i-1,0]
        daily_matrix[:,i,1] = matrix[:,i,2]
        
    return daily_matrix