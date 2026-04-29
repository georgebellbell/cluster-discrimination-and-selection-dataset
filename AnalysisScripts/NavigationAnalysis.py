from SharedAnalysisFunctions import *
from LoadAndPreprocessData import *
from scipy.stats import norm
from scipy import stats
import math
 
def compare_time_windows(dataset):
    results = []
    for cond in dataset["ViewingCondition"].unique():
        cond_data = dataset[dataset["ViewingCondition"] == cond]
        pivot = cond_data.pivot_table(
            index=["UserID", "TaskID", "Difficulty"],
            values=["avg_distance_first5", "avg_distance_next5"]
        ).dropna()

        early = pivot["avg_distance_first5"]
        late = pivot["avg_distance_next5"]

        diff = late - early

        shapiro = stats.shapiro(diff)
        test_name = "t-test" if shapiro.pvalue > 0.05 else "Wilcoxon signed-rank test"
        if shapiro.pvalue > 0.05:
            stat, p = stats.ttest_rel(early, late)
        else:
            stat, p = stats.wilcoxon(early, late)

        #print(f"Median early: {early.median():.4f}")
        #print(f"Median late: {late.median():.4f}")
        #print(f"Median change (late - early): {diff.median():.4f}")

        results.append({
            'Task': None,
            'ViewingCondition': cond,
            'Test': test_name,
            'Statistic': stat,
            'p-value': p,
            'MedianDistanceFirst5': early.median(),
            'MedianDistanceNext5': late.median(),
            'MedianDistanceChange': diff.median()
        })

    return results

def compute_time_averages(group):
    group = group.sort_values('TIMESTAMP')
    start = group['StartingTime'].iloc[0]
    rel_time = group['TIMESTAMP'] - start
    first5 = group[rel_time <= 3]['DistanceToA'].mean()
    next5 = group[(rel_time > 3) & (rel_time <= 6)]['DistanceToA'].mean()
    return pd.Series({'avg_distance_first5': first5, 'avg_distance_next5': next5})

df_movement = LoadMovementData()

time_based_averages = (
    df_movement
    .groupby(['UserID', 'TaskID','Task', 'ViewingCondition', 'Difficulty'], group_keys=False)
    .apply(compute_time_averages, include_groups = False)
    .reset_index()
)
time_based_averages = time_based_averages[['UserID', 'TaskID','Task', 'ViewingCondition', 'Difficulty',"avg_distance_first5", "avg_distance_next5"]].dropna()

metrics = ['LassoInteractions', 'RaycastInteractions', 'TotalLassoPoints', 'TotalRaycastPoints', 
            'LassoActionPercentage', 'RaycastActionPercentage', 'LassoPointsPercentage', 'RaycastPointsPercentage']

time_based_averages["DistanceDifference"] = time_based_averages["avg_distance_next5"] - time_based_averages["avg_distance_first5"]

viewing_angle = 10
group_cols = ['UserID', 'TaskID', 'Task', 'ViewingCondition', 'Difficulty']
lookData = df_movement.copy()

lookData["TimeProgressed"] = (
    lookData["TIMESTAMP"] - lookData["StartingTime"]
)

lookData["TimeDiff"] = (
    lookData.groupby(group_cols)["TimeProgressed"]
    .diff()
    .fillna(0)
)

lookData["AccumulatedLookTime"] = (
    lookData["TimeDiff"]
    .where((abs(lookData["ViewingAngleA"]) <= viewing_angle) | ((lookData["Task"] == "seperating") & (abs(lookData["ViewingAngleB"])<= viewing_angle)), 0)
    .groupby([lookData[col] for col in group_cols])
    .cumsum()
)
lookData  = lookData.groupby(['UserID','TaskID','ViewingCondition','Task','Difficulty', 'CompletionTime']).agg(
    AccumulatedLookTime=('AccumulatedLookTime', 'max')
).reset_index()
lookData["percentage_look_time"] = lookData["AccumulatedLookTime"] / lookData["CompletionTime"]

movement_change_results = []
viewpoint_looktime_comparison = []
viewpoint_looktime_difficulty_comparison = []
for task in ['denoising', 'seperating']:
    print(f"\nAnalyzing task: {task}")

    results = compare_time_windows(time_based_averages[time_based_averages['Task'] == task])
    for result in results:
        result['Task'] = task
        movement_change_results.append(result)
    
    task_dataset = lookData[lookData['Task'] == task]
    result = compare_viewpoints(pivot_and_calculate_diff(task_dataset, ['percentage_look_time']), 'percentage_look_time')
    result['Task'] = task
    viewpoint_looktime_comparison.append(result)

    results = check_difficulty_significance(task_dataset, 'percentage_look_time')
    for result in results:
        result['Task'] = task
        viewpoint_looktime_difficulty_comparison.append(result)



