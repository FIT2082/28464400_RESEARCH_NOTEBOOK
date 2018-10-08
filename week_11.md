1. Better accuracy results
2. Pictures of outcomes
3. Poster

# Week 11 Summary
We have great progress this week. We are now confident that our ARIMA Machine Learning Model works properly on most of the datasets we have tried and gives fairly accurate results. Our accuracy detecting algorithm is now fixed and now gives proper accuracy levels for our output. 

## Goals completed since last week
Since last week, we carried on the problem of getting a Machine Learning output that detects edges translated at a certain level off the actual edges, and now we have that problem fixed. Our accuracy algorithm does not give negative outcomes and is now limited within 0 to 100% accuracy levels. Our second part of the research, which was to implement and compare Machine Learning output with actual values is now complete.

## Research Conducted

### ARIMA Algorithm & Implementation
Finally, we have made massive improvements on our machine learning code since the start of writing our ARIMA Model code. We have multiple parameters that can be altered to give outputs giving better results compromising high computation power and longer time to produce outcomes. Even though the algorithm takes long to give an outcome, the results are immensely better than what we started off with. 

As shown below, the intensity graph plots the yellow points which are the areas between edges marked manually by Lachlan Andrew for us to compare our algorithms with.

![Python Script Edge Detection](/images/week10_savedrect.png)

The following graph shows the outcomes we recieve from our latest version of the ARIMA Model code. The results are very satisfactory with accuracy level of 69.01% which is much better than our expectations. For the output below, the Median Filtration level was kept at 11 and ARIMA Model Order of (0,0,0). The initial training dataset size is 2, which gave us good results for most datasets.

![Python Script Edge Detection](/images/week11_predicted.png)

### Accuracy Algorithm
Our accuracy algorithm flaws have now been corrected and tested on most datasets which gives proper results as illustrated below:

![Python Script Edge Detection](/images/week11_accuracyoutput.png)


## Goals before next meeting


