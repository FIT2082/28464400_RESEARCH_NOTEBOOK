# Week 9 Summary
This week, we had a look at what Time Series forecasting is, how they work in general cases, and how we can implement and use a good time series forecasting model for our project.

## Goals completed since last week
Based on the suggested Machine Learning algorithm of Auto Regressive Model, I researched on different statistical methods of machine learning algorithms in order to implement a Auto Regressive Model to our datasets to predict next values and detect edges.

## Research Conducted
This week, we did intensive research on Timeseries Forecasting. For our research, we plan to run our timeseries forecasting algorithm through each day of the year to detect the average value of electricity consumption. Basically creating a moving set of average values and then predicting the next value, and if this value is too high or too low compared to our prediction, we will mark it as an edge. This is the basic idea, and Auto Regressive Model is the best option for our case.

### ACF, PACF and MA Time Series
There are important properties of timeseries forcasting such as the ACF (Auto Correlation Function) and PACF (Partial Auto Correlation Function), and these two values can be used to understand the trend formed in the data being analysed.

Why is it important to our research? Because, if the PACF shows a very steady range of values, it is a great indication of our dataset following a time series called Moving Average (MA). In the case of MA, the ACF shows a single peak of value, and does not show a regular trend, indicating it is indeed an MA. These are extremely important in determining the estimator equation of the time series at it explains which previous values to take into consideration when creating the predictor equation. 




## Goals before next meeting
Still to be decided
