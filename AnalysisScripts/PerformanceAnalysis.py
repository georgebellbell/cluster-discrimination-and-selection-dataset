from SharedAnalysisFunctions import *
from LoadAndPreprocessData import *
from scipy.stats import norm
from scipy import stats
import math

def compute_sdt_metrics(TP, FP, TN, FN):
    """
    Compute d' and beta from confusion matrix counts.

    Parameters:
    TP: int - True Positives (hits)
    FP: int - False Positives (false alarms)
    TN: int - True Negatives (correct rejections)
    FN: int - False Negatives (misses)

    Returns:
    d_prime: float - sensitivity
    beta: float - decision bias
    """
    H = (TP + 0.5) / (TP + FN + 1)  # Hit rate
    F = (FP + 0.5) / (FP + TN + 1)  # False alarm rate

    # Compute z-scores
    zH = norm.ppf(H)
    zF = norm.ppf(F)

    # Compute d'
    d_prime = zH - zF

    # Compute beta
    beta = math.exp((zF**2 - zH**2) / 2)

    specificity = TN / (TN + FP) if (TN + FP) > 0 else 0

    return d_prime, beta, specificity

df_performance = LoadPerformanceData()
df_performance[['d_prime', 'beta', 'specificity']] = df_performance.apply(
    lambda row: compute_sdt_metrics(
        row['TruePositiveCount'], row['FalsePositiveCount'], row['TrueNegativeCount'], row['FalseNegativeCount']
    ),
    axis=1,
    result_type='expand' 
)

performance = df_performance.groupby(['UserID','ViewingCondition','Task','Difficulty']).agg(
    MeanAccuracy = ('Accuracy', 'mean'),
    StdDevAccuracy = ('Accuracy', 'std'),
    MeanPrecision = ('Precision', 'mean'),
    StdDevPrecision = ('Precision', 'std'), 
    MeanRecall = ('Recall', 'mean'),
    StdDevRecall = ('Recall', 'std'),
    MeanF1Score = ('F1Score', 'mean'),
    StdDevF1Score = ('F1Score', 'std'),
    MeanCompletionTime = ('CompletionTime', 'mean'),
    StdDevCompletionTime = ('CompletionTime', 'std'),
    MeanDPrime = ('d_prime', 'mean'),
    StdDevDPrime = ('d_prime', 'std'),
    MeanBeta = ('beta', 'mean'),
    StdDevBeta = ('beta', 'std'),
    MeanSpecificity = ('specificity', 'mean'),
    StdDevSpecificity = ('specificity', 'std'),
    MeanTruePositive = ('TruePositiveCount', 'mean'),
    StdDevTruePositive = ('TruePositiveCount', 'std'),
    MeanFalsePositive = ('FalsePositiveCount', 'mean'),
    StdDevFalsePositive = ('FalsePositiveCount', 'std'),

).reset_index()

performance_viewpoint_comparison = []
performance_difficulty_significance = []
performance_viewpoint_difficulty_comparison = []
metrics = ['MeanAccuracy', 'MeanPrecision', 'MeanRecall', 'MeanF1Score', 'MeanCompletionTime', 'MeanDPrime', 'MeanBeta', 'MeanSpecificity', 'MeanTruePositive', 'MeanFalsePositive']
for metric in metrics:
    print(f"\nAnalyzing metric: {metric}")
    for task in ['denoising', 'seperating']:
        print(f"\nAnalyzing task: {task}")
        
        task_dataset = performance[performance['Task'] == task]
        pivoted_dataset = pivot_and_calculate_diff(task_dataset, metrics)
        result = compare_viewpoints(pivoted_dataset, metric)
        result['Task'] = task
        performance_viewpoint_comparison.append(result)


        results =check_difficulty_significance(task_dataset, metric)

        for result in results:
            result['Task'] = task
            performance_difficulty_significance.append(result)

        results = compare_viewpoints_difficulties(task_dataset, metric)
        for result in results:
            result['Task'] = task
            performance_viewpoint_difficulty_comparison.append(result)