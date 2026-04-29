# The impact of viewpoint configuration on 3D cluster discrimination and selection

This repository contains the raw data, interview transcript data and data analysis scripts used in the paper.

Running the actions in CSAnalysis.ipynb will exectute different analyses on the datasets.

### Raw Data
This folder contains the raw data collected from the participant. This is split into three different CSV files:

- **Performance.csv** contains the metrics for how a participant did on a task, there is one entry per task.
- **MovementBehaviour.csv** contains the metrics for how the participant moved around the area, there are multiple entries per task
- **InteractionBehaviour.csv** contains the metrics for how the participant interacted with points within the scatterplot, there are multiple entries per task

### Analysis Scripts
This folder contains the scripts used to analyse the datasets:
- **LoadAndPreprocessData.py** & **SharedAnalysisFunctions** are shared files for loading the data and carrying out similar statistical tests respectively
- **PerformanceAnalysis.py** looks at the Performance data for different metrics looking for an effect from viewpoint as well as difficulty
- **NavigationAnalysis** looks at the Movement data, specifically how distance to a cluster changes over time and how long a participant spends looking at a cluster
- **SelectionAnalysis** looks at the Interaction data and how viewpoint effects the interaction technique used

### Analysis Data
This folder contains the formatted results of various statisical tests