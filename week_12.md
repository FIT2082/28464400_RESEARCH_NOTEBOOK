# Week 12 Summary
As planned, most of this week has been spent on creating the Poster, and discussing about the elevated pitch and presentation. The poster is already completed and we have visualized our Statistical Model that gave amazing results, and our Machine Learning algorithm that gives an accuracy of 68%.

## Goals completed since last week
Our priority for this week was to wrap up Statistical and ML model, and complete the poster file. We also changed our accuracy algorithm to include the aspects of True Positive and True Negative. As suggested by Dr. Mahsa, a better accuracy algorithm is created when we not only consider the True Positive values, rather, we use the a "Confusion Matrix", where we calculate True Positive (Number of Times our Model predicted the correct Edge), True Negative (The number of times our model correctly detected an incorrect edge), False Positive (Number of Times our Model incorrectly predicted the Edge), and the False Negative (Number of Times our Model incorrectly predicted a non-Edge when it was actualy an edge). This is illustrated in the following image. 

![Python Script Edge Detection](/images/week12_ConfusionMatrix.png)

We then use the heuristic based on the following formula to detect the accuracy of the ML Model:

![Python Script Edge Detection](/images/week12_classificationAccuracy.png)

## Poster

![Python Script Edge Detection](/images/28464400_Poster.png)

## Final Comments
We could successfully complete all the tasks as per the planning and the proposed timeline. With further improvements and possibilities of our research, there are potential to improve heuristics for statistical analysis, and to get better accuracy in ML results which can be done by adding more parameters and storing the training dataset collectively to store large training data. A better accuracy algorithm can be constructed using ROC curve as discussed with Dr. Mahsa, but due time constraints it remained beyond the scope of the research. Manually adding more validation data would be very beneficial to test variety of datasets using our models. 

Until week 14, me and Adolphus will be working on completing the Final Report for our project.

---- End of Project Notebook ----
