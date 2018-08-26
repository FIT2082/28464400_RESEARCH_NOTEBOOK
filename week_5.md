
# Week 5 Summary
This week we made good progress on our project. We worked mostly on our Python code to detect edges, and following Lachlan’s advice, we scanned 3500 house data sets to get statistics on the average durations for which timed devices were known to be kept on.

## Goals completed since last week
We refractored our Python code and now the code is much more organized. Since we started our Python code from scratch, we built several functions that does specific tasks and can be called individually.

## Meeting and Research conducted
Based on feedback on this week’s meeting, we have taken three tasks for this week all of them is to work on our Python code implementation. The first one is to implement a ‘median filter’ which is essentially a function to smoothen the edges detected and remove noises from locations where the edges are falsely detected. Adolphus has been focusing on that section of our task.

The next task is to analyse the timed electricity consumption data from the 3500 files that are prepared by Lachlan, and to get estimates of how long the timed devices are generally kept on, and the consecutive number of days for which they are used. I have been focusing on this part of our task, and I wrote functions to detect these variable data timings from the files. 

The following image shows the saved data obtained from a single house (house00002), and this data is already available in the variables of the .mat data files. These data can be used to compare our implementation and check accuracy of our code (which will be done later during the research as per the proposed schedule). Also, these known data can be used for supervised learning of Machine Learning algorithms that we will be implementing later.

![Python Script Edge Detection](/images/house0002_saved_data.png)

The next two images show the histograms of ‘day lengths’ and ‘time ranges’. These are the analysed data obtained from 3500 houses. These can potentially reveal a lot of information about the edge blocks for example, using this we know the ranges of the datasets where edge occurrences are higher, and can again be used in our supervised machine learning algorithms to get accurate results.

![Python Script Edge Detection](/images/day_lengths.png)

![Python Script Edge Detection](/images/time_ranges.png) 

## Goals before next meeting
The other task me and Adolphus will be working on is to detect half step edges and to calculate the mean-sd ratios of smaller chunks of data separately, before and after the edges. We can then compare these heuristic features to potentially find edges more accurately. There are further calculations involved with which Lachlan helped us in understanding. Our primary goal will be to implement these before the next meeting.
