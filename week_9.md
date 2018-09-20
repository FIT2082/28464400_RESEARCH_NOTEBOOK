# Week 9 Summary
This week, we had a look at what Time Series forecasting is, how they work in general cases, and how we can implement and use a good time series forecasting model for our project.

## Goals completed since last week
Based on the suggested Machine Learning algorithm of Auto Regressive Model, I researched on different statistical methods of machine learning algorithms in order to implement a Auto Regressive Model to our datasets to predict next values and detect edges.

## Research Conducted
This week, we did intensive research on Timeseries Forecasting. For our research, we plan to run our timeseries forecasting algorithm through each day of the year to detect the average value of electricity consumption. Basically creating a moving set of average values and then predicting the next value, and if this value is too high or too low compared to our prediction, we will mark it as an edge. This is the basic idea, and Auto Regressive Model is the best option for our case.

### ACF, PACF and MA Time Series
There are important properties of timeseries forcasting such as the ACF (Auto Correlation Function) and PACF (Partial Auto Correlation Function), and these two values can be used to understand the trend formed in the data being analysed.

Why is it important to our research? Because, if the PACF shows a very steady range of values, it is a great indication of our dataset following a time series called Moving Average (MA). In the case of MA, the ACF shows a single peak of value, and does not show a regular trend, indicating it is indeed an MA. These are extremely important in determining the estimator equation of the time series at it explains which previous values to take into consideration when creating the predictor equation. 

### ARIMA Algorithm & Implementation
Currently we have implemented the ARIMA (AutoRegressive Integrated Moving Average) algorithm in Python, which seperates a list of values into training (60%) and test (40%) dataset. Based on the training dataset, it predicts the testing dataset values and compares the actual values to calculate the MSE (Mean Squared Error). It then checks several values that ARIMA function takes to fit a polynomial function for prediction, and gets the set of values with minimum MSE. That way we know the predictions are as accurate as possible.

### ARIMA Algorithm Outcomes
The following picture shows the initial intensity graph on which we tested out ARIMA code:

![Python Script Edge Detection](/images/week_9_original.png)

When we implemented ARIMA algorithm with order of (0,0,0), with taking an average of 3 consecutive values and predicting the next ones, plotted with Median Filter at filtration level of 11, we got the following outcome:

![Python Script Edge Detection](/images/week9_arima_3_filt_11.png)

Again, we implemented ARIMA algorithm with order of (0,0,0), with taking an average of 6 consecutive values and predicting the next ones, plotted with Median Filter at filtration level of 5, we got the following outcome:

![Python Script Edge Detection](/images/week9_arima_6_filt_5.png)

These show good results in detecting the edges, but there is ample space for improvement. Since this week we implemented the Moving Average Machine Learning Model, we can change the order of the model which will be learnt from the data observed. Once the order is learnt by the algorithm, the algorithm will keep giving more and more accurate results. This is one of the parameters which we will keep on improving. Also, the number of averages we take each time we make a prediction can be varied to check which one gives the most accurate outcomes. The noises in the data is removed using the previously used Median filter. 

## Goals before next meeting
We have successfully implemented the Autoregression Model that we aimed for last week. There are parameters which can surely be improved and we plan on improving this model as much as we can by the end of next week. Up until now, our progress is on track and we are satisfied with what we have achieved so far.

