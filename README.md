# The impact of viewpoint configuration on 3D cluster discrimination and selection

This repository contains the raw data, interview transcript data and data analysis scripts used in the paper.

Running the actions in CSAnalysis.ipynb will exectute different analyses on the datasets.

## Raw Data
This folder contains the raw data collected from the participant. This is split into three different CSV files:

- **Performance.csv** contains the metrics for how a participant did on a task, there is one entry per task.
    - TIMESTAMP: Time, in seconds, for amount of time experiment has been running
    - UserID: Unique identifier for a participant
    - TaskID: Identifier for a unique participant's task
    - ViewingCondition: Whether the task was carried out in an egocentric or exocentric viewpoint
    - Task: Whether the task carried out was denoising (distinction) or seperation
    - Difficulty: The level of challenge of a given task (EASY, MEDIUM, HARD)
    - TaskPhase: Whether the task was training (had validation) or was the actual task
    - TruePositiveCount: Number of points the participant correctly identified as belonging to a cluster
    - TrueNegativeCount: Number of points the participant correctly identified as not belonging to a cluster
    - FalsePositiveCount: Number of points the participant incorrectly identified as belonging to a cluster
    - FalseNegativeCount: Number of points the participant incorrectly identified as not belonging to a cluster
        - Precision, Recall, Accuracy & F1Score: additional metrics calculated from previous four metrics 
    - Completion Time: total amount of time, in seconds, spent on a given task
- **MovementBehaviour.csv** contains the metrics for how the participant moved around the area, there are multiple entries per task sampled every 0.5 seconds
    - TIMESTAMP: Time, in seconds, for amount of time experiment has been running
    - UserID: Unique identifier for a participant
    - TaskID: Identifier for a unique participant's task
    - DistanceToA: Total distance to first, or single, cluster
    - ViewingAngleA: Angle difference between the view direction of the participant and the direction to a cluster from the participant
    - DistanceToB: Total distance to second, cluster
    - ViewingAngleB: Angle difference between the view direction of the participant and the direction to second cluster from the participant
    - UserPosition(X,Y and Z): current location of participant throughou the experiment

- **InteractionBehaviour.csv** contains the metrics for how the participant interacted with points within the scatterplot, there are multiple entries per task. Each entry represents an interaction update.
    - TIMESTAMP: Time, in seconds, for amount of time experiment has been running
    - UserID: Unique identifier for a participant
    - TaskID: Identifier for a unique participant's task
    - RaycastCount: The number of elements selected with the raycast technique. If it contains a value greater than 0 then the interaction is a raycast
    - LassoCount: The number of elements selected with the lasso technique. If it contains a value greater than 0 then the interaction is a lasso
    - SelectedACount: The number of points currently selected as belonging to the first cluster
    - SelectedBCount: The number of points currently selected as belonging to the second cluster
    - UnselectedCount: The number of points that have not been selected as belonging to either cluster. Starting value is equal to the total number of points in the task.
## Analysis Scripts
This folder contains the scripts used to analyse the datasets:
- **LoadAndPreprocessData.py** & **SharedAnalysisFunctions** are shared files for loading the data and carrying out similar statistical tests respectively
- **PerformanceAnalysis.py** looks at the Performance data for different metrics looking for an effect from viewpoint as well as difficulty
- **NavigationAnalysis** looks at the Movement data, specifically how distance to a cluster changes over time and how long a participant spends looking at a cluster
- **SelectionAnalysis** looks at the Interaction data and how viewpoint effects the interaction technique used

## Analysis Data
This folder contains the formatted results of various statisical tests

## Qualitative Data
This folder contains transcribed interview findings, categorised based on relevance to task and viewpoint