1. Accuracy Algorithm
2. Constantly getting a set of values that lay outside the expected area


# Week 10 Summary
We invested this week on improving the ARIMA Machine Learning algorithm, and we have an accuracy measuring algorithm that properly detects the accuracy of our Machine Learning Algorithm compared to the actual datasets stored within the MATLAB variable of the datasets as 'savedrects'.

## Goals completed since last week
From previous week, we were making the mistake of not adding all the data to our training list, as the time series forecasting algorithm ran along the dataset. We made fixes on the code and found several bugs that made our Machine Learning Algorithm much better. However, there is still an error we are constantly getting for our dataset which is explained below.

## Research Conducted

### Accuracy Algorithm
Currently we have implemented an Accuracy algorithm that goes through each of the data of the actual matrix and the predicted matrix so that the rate of accurate predictions made can be calculated. How it works is basically it calculates the number of common 'yellow' points of the intensity graphs and calculates the percentage of these points against the total 'yellow' points in the dataset that has the edges already identified. This way the accuracy of our predicted intensity graph edges can be compared accurately.

### ARIMA Algorithm & Implementation
Currently we have made the algorithm much more flexible. Last week, we implemented the training list so that it makes predictions based on the training data size we specified and the training list would not grow. Currently our algorithm adds all the data that it detects to be non-edges to the training list and makes predictions from this growing list to get better in prediction as it progresses. We know that more data means better model fitting, and hence our algorithm gets better as it progresses through the dataset. The training data size can be initially set to any number that gives better accuracy, but as far as we have seen from the outcomes, 2 is a good compromise. Following from last week, we can also adjust the order for ARIMA model and Median Filtration level.

However, despite all the improvements, we have seen a noticable level of translation of the detected edges from the actual edges. As illustrated below, we could not find the reason or the code for which this translation is constantly seen on all of our datasets. We will have a look into this next week and hopefully fix it quickly before the poster session.

![Python Script Edge Detection](/images/week10_translated.png)

For the above dataset the Median Filtration level was kept at 11 and ARIMA Model Order of (0,0,0). However, the intensity map given below is the outcome that is plotted from the data of savedrects which shows the actual rectangles that should be detected (this data was manually recorded by Lachlan Andrew). Currently, comparing these two intensity graphs, the accuracy algorithm gave us an accuracy rate of our predicted model to be 27%.

![Python Script Edge Detection](/images/week10_savedrect.png)

Another flaw we currently have is with the Accuracy algorithm. For some of the datasets we get negative accuracy level which is very dissapointing. There must be some flaw in the implementation of the accuracy algorithm that gives a false output, but we will look into that next week.

The noise from last weeks implementations are removed at a satisfactory level using Median Filter. However, we plan to tweak different parameters and get accuracy results that can be presented well.

## Goals before next meeting
Our primary goal would be to fix the translation problem with the intensity graph and improve the accuracy detecting algorithm so that accurate results are obtained. We have also started the discussion regarding the Poster that needs to be ready with visualizations and writings. We will work on that next week.

