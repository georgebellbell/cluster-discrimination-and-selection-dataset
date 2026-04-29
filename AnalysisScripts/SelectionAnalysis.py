from SharedAnalysisFunctions import *
from LoadAndPreprocessData import *
from scipy.stats import norm
from scipy import stats
import math

df_interaction = LoadInteractionData()

df_interaction = df_interaction.groupby(
    ['UserID', 'TaskID', 'ViewingCondition', 'Task', 'Difficulty']
).agg(
    LassoInteractions=('LassoCount', lambda x: (x > 0).sum()),
    RaycastInteractions=('RaycastCount', lambda x: (x > 0).sum()),
    TotalLassoPoints=('LassoCount', 'sum'),
    TotalRaycastPoints=('RaycastCount', 'sum'),
).reset_index()

df_interaction['TotalActions'] = df_interaction['LassoInteractions'] + df_interaction['RaycastInteractions']    
df_interaction['TotalPoints'] = df_interaction['TotalLassoPoints'] + df_interaction['TotalRaycastPoints']

df_interaction['LassoActionPercentage'] = df_interaction['LassoInteractions'] / df_interaction['TotalActions']
df_interaction['RaycastActionPercentage'] = df_interaction['RaycastInteractions'] / df_interaction['TotalActions']

df_interaction['LassoPointsPercentage'] = df_interaction['TotalLassoPoints'] / df_interaction['TotalPoints']
df_interaction['RaycastPointsPercentage'] = df_interaction['TotalRaycastPoints'] / df_interaction['TotalPoints']

selection_viewpoint_comparison = []

metrics = ['LassoInteractions', 'RaycastInteractions', 'TotalLassoPoints', 'TotalRaycastPoints', 
            'LassoActionPercentage', 'RaycastActionPercentage', 'LassoPointsPercentage', 'RaycastPointsPercentage']


for metric in metrics:
    print(f"\nAnalyzing metric: {metric}")
    for task in ['denoising', 'seperating']:
        print(f"\nAnalyzing task: {task}")
        task_dataset = df_interaction[df_interaction['Task'] == task]
        pivoted_dataset = pivot_and_calculate_diff(task_dataset, metrics)
        result = compare_viewpoints(pivoted_dataset, metric)
        result['Task'] = task
        selection_viewpoint_comparison.append(result)
