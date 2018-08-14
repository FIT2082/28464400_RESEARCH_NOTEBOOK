# Week 3 Summary
We had our second meeting this week with my research supervisor Lachlan Andrew, and my research partner Adolphus Lee. This week we discussed about h

## Goals completed since last week
As planned, we are still working on converting the MATLAB code into Python. On looking into several methods for edge detection, we researched on specific methods of machine learning including classification for images, decision trees, logic regression models, Long Short Term Memory, and LASSO. While some of these can be used to detect the plunges or surges of electricity, some would not be useful.

## Meeting and Research conducted
Both me and Adolphus have looked into and understood the datasets. We explored different machine learning techniques and probed into the implementation details of different models and implementations. We are researching to detect edges in two possible ways. The first way is to use the images generated from the datasets using image recognition, alternatively we can use the value datasets in order to understand the values that cause the edges to form. One of the important tasks we also worked on this week is the Project Specification that needs to be submitted by this Friday. We haven't finished it yet, but we will continue to work on it this week as well.

###  Edge Detection librares in MATLAB
I was exploring MATLAB built in functions to try to detect edges in our intensity image, and we used Canny and Prewitt methods. However, the resulting image is bad at understanding the horizontal edges in the default image, therefore we could conclude after several trials that using the libraries of MATLAB would not be of much help to our project.

The following image is the default image that results from the dataset

![Default Image](/images/default_test_image.png)

The following image is the image that results from running the canny and prewitt edge detection methods respectively, using MATLAB library. As clearly it can be seen, the edge detections are not accurate and it fails to detect most horizontal edges from the default picture.

![Canny Prewitt Edge Detection](/images/canny_prewitt_edgedetection.png)

### Python Script to detect edges
Me and Adolphus have worked on writing a Python script that detects edges and marks them in yellow by calculations involving standard deviation for each days. The following image shows the results, but once again, the accuracy is very low.

![Python Script Edge Detection](/images/week2_python.png)

## Goals before next meeting
Since we could not properly work on converting the initial MATLAB code into Python this week, this will still be our top most priority for next week's goals. Also, the accuracy of the previous implemenetations are poor and hencewe aim to probe further down our research into detecting edges using LSTM or Image classifiers. We will keep on implementing new things to try to get the most optimal results. However, we will be showing all of our progress to Lachlan on our next meeting.
