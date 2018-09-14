
# Week 6 Summary
Based on our previously set goals, optimization was the key objective for this week's work. 

## Goals completed since last week
According to Lachlan, Minimum filter or Median filter are good methods of reducing noise in our generated images. This week's work focuses on removing noise.

## Research conducted
Working on our Python code, we researched on filtration methods to remove unnecessary noises from our dataset. Two great options for our problem of noise includes median or minimum filter. Within these filters, different levels of filtration produces different level of clarity of data, so we researched on going through these values to find the best filter and filtration level. Some of them are as follows:

At first, we tried applying Median filter. The follwing image shows the median filter working on our noisy data at the filtration level of 9:

![Python Script Edge Detection](/images/MedianFilter_9.png)

We can compare this with the Median filter applied in the following image but at the filtration level of 99:

![Python Script Edge Detection](/images/MedianFilter_99.png)

The next two images show the same levels of filtration but this time using Minimum filters:

![Python Script Edge Detection](/images/MinimumFilter_9.png)

![Python Script Edge Detection](/images/MinimumFilter_99.png)

Noticable from the above images, minimum filtration level of 99 removes most of the points from our dataset, which is undesirable.

## Goals before next meeting
