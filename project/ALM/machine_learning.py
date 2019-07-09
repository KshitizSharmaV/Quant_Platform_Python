# Importing basic python packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime as dt
import talib
import statsmodels.api as sm
import json
from sklearn import metrics
from sklearn.tree import DecisionTreeRegressor



def building_features(data):
	data['5DayFutureClose']=data['Adj Close'].shift(-5)
	data['5DCloseFuture%']=data['5DayFutureClose'].pct_change(5)
	data['5DClose%']=data['Adj Close'].pct_change(5)
	data['Volume_1D_Change']=data['Volume'].pct_change()
	data['Volume_1D_Change_5_SMA']=talib.SMA(data['Volume_1D_Change'],timeperiod=5)

	target_names=['5DCloseFuture%']
	features_names=['5DClose%','Volume_1D_Change','Volume_1D_Change_5_SMA']

	for n in [14,30,50,200]:
	    # Create a Moving Average indicator & divide by Adj Close
	    data['ma'+str(n)]=talib.SMA(data['Adj Close'].values, timeperiod=n)/data['Adj Close']
	    
	    # Create a RSI indicator & divide by Adj Close
	    data['rsi'+str(n)]=talib.RSI(data['Adj Close'].values,timeperiod=n)
	    
	    # MA & RSI to features_names
	    features_names = features_names+['rsi'+str(n),'ma'+str(n)]
    
	# Lets drop the NA values which will mess up with ML model otherwise
	data=data.dropna()

	days_of_weeks= pd.get_dummies(data.index.dayofweek,prefix='weekday',drop_first=True)
	days_of_weeks.index=data.index

	data=pd.concat([data,days_of_weeks],axis=1)

	features_names.extend(['weekday_' + str(i) for i in range(1, 5)])
	data=data.dropna()

	print("Features Names")    
	print(features_names)
	print("**************")
	print("Dataset")        
	print(data.head(5))


	# Declare target and features
	target=data['5DCloseFuture%']
	features=data[features_names]

	#Features_Target_Data
	Features_Target_Data=data[['5DCloseFuture%']+features_names]

	# Find the correlation between targets and features
	print("Correlation Between Features And Targets")
	Corr=Features_Target_Data.corr()
	return target,features


def linear_regression(target,features):
	linear_features=sm.add_constant(features)

	train_size=int(0.85*linear_features.shape[0])
	train_targets=target[:train_size]
	train_features=features[:train_size]
	test_targets=target[train_size:]
	test_features=features[train_size:]

	model=sm.OLS(train_targets,train_features)
	results=model.fit()
	
	pvalues=dict(round(results.pvalues,3))
	coeff=dict(round(results.params,3))
	r_square_adj=round(results.rsquared_adj,3)

	train_predictions = results.predict(train_features)
	test_predictions = results.predict(test_features)

	r2_score_test=metrics.r2_score(test_targets,test_predictions)

	train_target_features=list(zip(list(round(train_predictions,3)),list(round(train_targets,3))))
	test_target_features=list(zip(list(round(test_predictions,3)),list(round(test_targets,3))))

	linear_results={'pvalues':pvalues,'coeff':coeff,'Adj. R-squared':r_square_adj,'Test data score':r2_score_test,'train_target_features':json.dumps(train_target_features),'test_target_features':json.dumps(test_target_features)}
	
	return linear_results

def Decision_Tree_Regressor(target,features):
	train_size=int(0.85*target.shape[0])
	train_targets=target[:train_size]
	train_features=features[:train_size]
	test_targets=target[train_size:]
	test_features=features[train_size:]

	print(train_features)

	model=DecisionTreeRegressor()
	model.fit(train_features,train_targets)
	train_score=model.score(train_features,train_targets)
	test_score=model.score(test_features,test_targets)



	decision_tree_results={'train_score':train_score,'test_score':test_score}
	return decision_tree_results



