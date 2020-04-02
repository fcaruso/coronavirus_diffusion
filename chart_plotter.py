import numpy
import matplotlib 
import matplotlib.pyplot as pl
from matplotlib import dates
from matplotlib.dates import DayLocator, HourLocator, DateFormatter, drange

# plot reional charts
def plot_regional_charts(list_dates, list_regions, matrix, concentration_matrix, output_dir, file_prefix):
    [ n_rows, n_cols ] = concentration_matrix.shape

    matplotlib.rcParams.update({'font.size': 16})
    bar_width = 0.2 # width of the plot's bars
    list_dates_offset_left  = [ e - bar_width / 2 for e in list_dates ]
    list_dates_offset_right = [ e + bar_width / 2 for e in list_dates ]
        
    for i in range(len(list_regions)):
        fig = pl.figure(figsize=(12,6))
        cp = pl.subplot()
        cp.set_title( list_regions[i] )
        ax = pl.gca()
        pl.xticks(rotation=90)
        line_ratios = cp.plot_date(list_dates, concentration_matrix[i], linestyle='solid', label='percentuale tamponi positivi')
        cp.xaxis.set_major_locator(DayLocator())
        cp.xaxis.set_major_formatter(DateFormatter("%m-%d"))
        cp.legend(loc='upper left',bbox_to_anchor=(0.,.9,.8,.1))
        ax.set_ylabel("% Positivi")

        cp2 = pl.twinx()
        rects_swabs     = cp2.bar(list_dates_offset_left, matrix[i,:,0], bar_width, color="green")
        rects_positives = cp2.bar(list_dates_offset_right, matrix[i,:,1], bar_width, color="red")
        cp2.legend( ( rects_swabs, rects_positives), ("tamponi", "tamponi positivi"),loc='upper left',bbox_to_anchor=(0., 0.8,0.8,0.1) )
        ax2 = pl.gca()
        ax2.set_ylabel(" Tamponi ")
        filename = list_regions[i] + ".png"
        fig.savefig(output_dir+file_prefix+filename)
        pl.close()

def plot_national_charts(list_dates, list_regions, concentration_matrix, matrix, output_dir, file_prefix):
    [n_rows, n_cols] = concentration_matrix.shape

    array_concentration = [ el for el in numpy.sum( concentration_matrix, 0 )/n_rows ]
    array_swabs = [ el for el in numpy.sum(matrix[:,:,0],0 ) ] 
    array_positives = [ el for el in numpy.sum(matrix[:,:,1],0) ]

    matplotlib.rcParams.update({'font.size': 24})
    fig = pl.figure(figsize=(24,10))
    cp = pl.subplot()
    ax = pl.gca()
    pl.xticks(rotation=90)
    cp.xaxis.set_major_locator(DayLocator())
    cp.xaxis.set_major_formatter(DateFormatter('%d-%m'))
    cp.plot_date(list_dates,array_concentration, linestyle='solid',label="percentuale tamponi positivi")
    ax.set_ylabel("% Positivi ")
    cp.legend(loc='upper left',bbox_to_anchor=(0.,.9,0.8,0.1))

    cp2 = pl.twinx()

    bar_width = 0.2 # width of the bars
    list_dates_offset_left  = [ e - bar_width / 2 for e in list_dates ]
    list_dates_offset_right = [ e + bar_width / 2 for e in list_dates ]
    rects_swabs = cp2.bar(list_dates_offset_left, array_swabs, bar_width, label='Tamponi',color="green")
    rects_positives = cp2.bar(list_dates_offset_right, array_positives, bar_width, label="Positivi",color="red")
    cp2.legend( ( rects_swabs, rects_positives), ("tamponi", "tamponi positivi"),loc='upper left',bbox_to_anchor=(0., 0.8,0.8,0.1) )
    ax2 = pl.gca()
    ax2.set_ylabel(" Tamponi ")
    fig.savefig(output_dir+file_prefix+".png")
    pl.close()

def plot_regional_daily_charts(list_dates, list_regions, daily_matrix, daily_concentration_matrix, output_dir, file_prefix):
    [n_rows, n_cols, z] = daily_matrix.shape

    matplotlib.rcParams.update({'font.size': 16})
    bar_width = 0.2 # width of the plot's bars
    list_dates_offset_left  = [ e - bar_width / 2 for e in list_dates ]
    list_dates_offset_right = [ e + bar_width / 2 for e in list_dates ]
        
    for i in range(len(list_regions)):
        fig = pl.figure(figsize=(12,6))
        cp = pl.subplot()
        cp.set_title( list_regions[i] )
        ax = pl.gca()
        pl.xticks(rotation=90)
        line_ratios = cp.plot_date(list_dates, daily_concentration_matrix[i], linestyle='solid', label='percentuale tamponi positivi')
        cp.xaxis.set_major_locator(DayLocator())
        cp.xaxis.set_major_formatter(DateFormatter("%m-%d"))
        cp.legend(loc='upper left',bbox_to_anchor=(0.,.9,.8,.1))
        ax.set_ylabel("% Positivi")

        cp2 = pl.twinx()
        rects_swabs     = cp2.bar(list_dates_offset_left, daily_matrix[i,:,0], bar_width, color="green")
        rects_positives = cp2.bar(list_dates_offset_right, daily_matrix[i,:,1], bar_width, color="red")
        cp2.legend( ( rects_swabs, rects_positives), ("tamponi", "tamponi positivi"),loc='upper left',bbox_to_anchor=(0., 0.8,0.8,0.1) )
        ax2 = pl.gca()
        ax2.set_ylabel(" Tamponi ")
        filename = list_regions[i] + ".png"
        fig.savefig(output_dir + file_prefix + filename)
        pl.close()

# bar-plot the concentration of (positive cases)/(number of swabs) for each region
def plot_regional_averages(list_regions, concentration_matrix, output_dir, file_prefix):
    y_val = len(list_regions)
    array_averages = [ el for el in numpy.average(concentration_matrix[:,:],1 ) ] 
    map_averages = {}
    for i in range(y_val):
        map_averages.update({list_regions[i]:array_averages[i]})
    
    sorted_average_map = {k: v for k, v in sorted(map_averages.items(), key=lambda item: item[1])}
    fig = pl.figure(figsize=(24,10))
    cp = pl.subplot()
    ax = pl.gca()

    pl.bar(list(sorted_average_map.keys()), list(sorted_average_map.values()) )
    pl.xticks(rotation=90)
    ax.set_ylabel("% Positivi")

    fig.savefig(output_dir + file_prefix + "media_regionale", bbox_inches='tight')
    pl.close()