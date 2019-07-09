import pandas as pd
import numpy as np
from scipy.stats import skew,kurtosis,shapiro
import collections

# This file consists of the functions and calculations which are being published on page. The functions 
# below are called from views.py file

def load_data_set(data):
	ticker='TSLA'
	data=pd.read_csv("Data/TSLA.csv")
	return data


def clean_price_dataframe(data):
	data.index=data['Date']
	data.index=pd.to_datetime(data.index)

	data['years']=data.index.year
	data['months']=data.index.month
	data['groupindex']=data['years']-min(set(data['years']))

	data['Returns']=(data['Close'].pct_change())*100
	data=data.dropna()
	data['Date']=pd.to_datetime(data['Date'])
	
	return data

def stock_analysis(data):
	mean_return_daily = np.mean(data['Returns'])
	mean_return_annualized = (((1+mean_return_daily)**252)-1)
	mean_return_annualized=float('{0:.20f}'.format(mean_return_annualized))


	sigma_daily = np.std(data['Returns'])
	variance_daily = np.square(sigma_daily)

	sigma_annualized = sigma_daily*np.sqrt(252)
	variance_annualized = np.square(sigma_annualized)

	returns_skewness = skew(data['Returns'])

	excess_kurtosis = kurtosis(data['Returns'])
	returns_kurtosis = 3+excess_kurtosis

	shapiro_results = shapiro(data['Returns'])
	p_value_shapiro_results = shapiro_results[1]

	print(mean_return_annualized)

	metrics={'Last price':248.1,'Mean Daily Return':mean_return_daily,'Variance Daily':variance_daily,'Variance Annualized':variance_annualized,'Skewness':returns_skewness,'kurtosis':excess_kurtosis,'Shapiro P-Value':p_value_shapiro_results}
	for key,value in metrics.items():
		metrics[key]=round(value,2)

	return metrics


def by_year_performance(data):
	years_list=list(set(data.index.year))
	years_list.sort()

	temp=data.groupby('years')

	bee_plot_years_list=list(set(data.index.year))
	# Categories
	bee_plot_years_list.sort()
	# Scatter Data
	bee_plot_scatter=data[['groupindex','Returns']].to_json(orient='values')


	t={}
	bee_plot_percentiles = []
	scatter_plot_ranking=[]
	count=0
	for i in temp.groups.keys():
	    d=list(temp.get_group(i)['Returns'])
	    d.sort()
	    scatter_plot_ranking.append(list(temp.get_group(i)['Returns'].rank(pct=True)+count-0.5))
	    t=[np.percentile(d,0),np.percentile(d,25),np.percentile(d,50),np.percentile(d,75),np.percentile(d,100)]
	    bee_plot_percentiles.append(t)
	    count=count+1

	scatter_plot_ranking_flat=[item for sublist in scatter_plot_ranking for item in sublist]
    
	print(len(scatter_plot_ranking_flat))
	data['scatter_plot_ranking']=scatter_plot_ranking_flat

	bee_plot_scatter=data[['scatter_plot_ranking','Returns']].to_json(orient='values')

	bee_swarm_box_plot={'bee_plot_years_list':bee_plot_years_list,'bee_plot_scatter':bee_plot_scatter,'bee_plot_percentiles':bee_plot_percentiles}	    

	return bee_swarm_box_plot


def time_interval_performance(data,start_date,end_date):
	time_period = [5,10,15,30,60,90,120,252]
	perf=[]
	performance=[]
	for i in time_period:
		temp=data.tail(i)
		total_return=np.round(temp['Returns'].sum(),2)
		price_min=np.round(min(temp['Close']),2)
		price_max=np.round(max(temp['Close']),2)
		sigma_daily = np.std(temp['Returns'])
		variance_daily = np.round(np.square(sigma_daily),2)
		perf.append([i,total_return,price_min,price_max,variance_daily])
	header=[u'Days',u'Return',u'Min Close',u'Max Close',u'Variance']
	performance={
	'headers':header,
	'rows':perf
	}
	print(performance)
	return performance

def top_performing_indicators(data):
	top_indicators=['RSI 20','MA 20','RSSI 40','MA 40']
	return top_indicators













