# Week 4 Summary
We had our group meeting this week with my research supervisor Lachlan Andrew, and my research partner Adolphus Lee, and many other researchers working in a similar project to ours. These group meetings are very helpful since they allow us to discuss our progress and we can find better ways of collaborating our work for productive results.

## Goals completed since last week
We made remarkable progress on our Python code, however, we decided to start from scratch and implement our own Python function instead of converting the code. This way we will have more knowledge on the implementation of the code which can benefit us later on. We continued reading further into methods of LSTM and Image classifiers, however based on our estimated timeline of our research, we are focusing on the main features to distinguish the edges for this week.

## Meeting and Research conducted
Since our Project Specification is due by the end of this week, we have spent a great deal of time working on it. We have realized that trying to get the edges solely based on mean-sd ratio of consecutive data elements give a high number of false outputs. We have been, and still are implementing different calculations in trying to find a proper heuristic using which we can detect the edges.

## Proposed Timeline
### Week 2
Understanding the project requirements, exploring different ways to detect edges and proposing them to the research supervisor, literature review on different machine learning including image recognition techniques and statistics

### Week 3
Understanding the resources and data available and getting the initial MATLAB code to set up. Re-writing MATLAB code to Python to primarily detect edges, and finding examples where mean:sd does not work to establish the research question

### Week 3 -5
Implementing and optimising Python code to properly replicate the MATLAB code. Statistical methods of mean:sd ratio with other calculations are still to be tested to find out better features and calculations of detecting edges

### Week 6 - 10
Implementing Machine learning algorithms including Image classification, Logic Regression and LSTM classification methods. We will continue to find the right features to detect edge candidates accurately, we will implement these techniques on the previous samples where mean:sd failed

### Week 10 - 12
Comparing all the implementations and outcomes to discard unreliable and failed implementations. Running benchmark tests and comparing datasets with human vision to determine accuracy. Final changes and revisions made to the implementation of edge detection method. Writing Final Report

### Week 11
Presentation of the project and discussion about writing Final Report

### Modifications to Python Script to detect edges
In our Python code, we implemented day wise (horizontal) calculations rather than the half hourly (vertical) calculations that were implemented last week. This was recommended to us by our supervisor in order to get a better estimate as edge heuristics. The following image shows results obtained from this implementation, however the results will be judged by Lachlan in order to decide the better way to proceed forward.

![Python Script Edge Detection](/images/week4.png)

## Goals before next meeting
We will try to implement the Python code to start detecting edges. Also, the accuracy of the previous implementations are poor and hence, we aim to probe further down our research into detecting edges using LSTM or Image classifiers. We will keep on implementing new things to try to get the most optimal results. However, we will be showing all of our progress to Lachlan on our next meeting.
