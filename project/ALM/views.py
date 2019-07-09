from django.shortcuts import render
from django.http import HttpResponse
from ALM.Views_Actions import *
from ALM.machine_learning import *

# Importing basic python packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime as dt

# Create your views here.
def index(request):
	print("Hello")
	return render(request,'WebFiles/index.html')

# Test function
def analytics(request):
	return render(request,'WebFiles/analytics.html')

# Main introduction page where company information shows up and technical analysis of company
# All functions for it are present in View_Actions.py
def Tech_Analytics(request):
	# load the data set
	ticker='TSLA'
	data=load_data_set(ticker)

	# Calling the function to clean the data in Views_action.py
	data=clean_price_dataframe(data)

	# Get returns from the close prices 
	returns=list(data['Returns'])

	# Give chart title 
	chart_title_1=ticker + " price chart"
	chart_title_2=ticker + " returns chart"
	
	#  lines below should appear together don't change the sequence of it
	prices_data=data[['Date','Close']].to_json(orient='values')
	returns_data=data[['Date','Returns']].to_json(orient='values')

	# Calculate metrics and returns 
	metrics=stock_analysis(data)

	# Calculations for Bee Swarm / Box Plots
	bee_swarm_box_plot_yearly=by_year_performance(data)
	time_interval_perform=time_interval_performance(data,'NULL', 'NULL')
	top_indicators=top_performing_indicators(data)
	context={'data':prices_data,'returns_data':returns_data,'returns':returns,'chart_title_1':chart_title_1,'chart_title_2':chart_title_2,'metrics':metrics,'bee_swarm_box_plot_yearly':bee_swarm_box_plot_yearly,'time_interval_perform':time_interval_perform,'top_indicators':top_indicators}
	
	return render(request,'WebFiles/Tech_Analytics.html',context)

# All major functions are present in machine_learning.py
def Machine_Learning(request):
	ticker='TSLA'
	# below functions in Views Action
	data=load_data_set(ticker)
	data=clean_price_dataframe(data)

	# Call the function in machine_learning.py to build features
	target,features=building_features(data)

	# Linear regression
	linear_regression_results=linear_regression(target,features)

	# Decision Tree Regressor
	decision_tree_results=Decision_Tree_Regressor(target,features)

	context={'target_name':'5DCloseFuture%','features_name':list(features.columns),'linear_regression_results':linear_regression_results,'decision_tree_results':decision_tree_results}
	return render(request,'WebFiles/Machine_Learning.html',context)

def Modelling(request):
	print("Hello")
	return render(request,'WebFiles/Modelling.html')

def Statistical_Analysis(request):
	print("Hello")
	return render(request,'WebFiles/Statistical_Analysis.html')

def Time_Series(request):
	print("Hello")
	return render(request,'WebFiles/Time_Series.html')

def Portfolio(request):
	print("Hello")
	return render(request,'WebFiles/Portfolio.html')

def Special_Events(request):
	print("Hello")
	return render(request,'WebFiles/Special_Events.html')

def Unstructured_data(request):
	print("Hello")
	return render(request,'WebFiles/Special_Events.html')









