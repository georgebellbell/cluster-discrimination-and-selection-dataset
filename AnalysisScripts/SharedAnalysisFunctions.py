from statsmodels.stats.anova import AnovaRM
from scipy import stats
import itertools
import numpy as np

def compare_for_normality(dataset, metric, log_result = False):
    conditions = ['EGOCENTRIC', 'EXOCENTRIC']
    difficulties = ['EASY', 'MEDIUM', 'HARD']
    
    normal = True
    for cond in conditions:
        for diff in difficulties:
            values = dataset[(dataset['ViewingCondition']==cond) & (dataset['Difficulty']==diff)][metric]
            if len(values) < 3:
                continue
            stat, p = stats.shapiro(values)
            if p < 0.05:
                normal = False

            if log_result:
                print(f"{cond}:Shapiro-Wilk: {cond} {diff} p = {p:.4f}")
    
    return normal


def difficulty_pairwise_wilcoxon(data, metric, viewing_condition):
    #print(f"\nPost-hoc Wilcoxon tests for {metric} under {viewing_condition} condition:")
    data = data[data["ViewingCondition"] == viewing_condition]

    difficulty_order = ("EASY", "MEDIUM", "HARD")
    pivot = data.pivot_table(
        index="UserID",
        columns="Difficulty",
        values=metric
    ).dropna()
    results = []
    for d1, d2 in itertools.combinations(difficulty_order, 2):
        #print(f"\n{d1} vs {d2} for {metric} under {viewing_condition}:")

        subset = pivot[[d1, d2]].dropna()

        d1_values = subset[d1]
        d2_values = subset[d2]


        stat, p = stats.wilcoxon(d1_values, d2_values)
        results.append(
            {
                'Task': None,
                'Metric': metric,
                'ViewingCondition': viewing_condition,
                'FriedmanChi2': None,
                'FriedmanP': None,
                'Difficulty': f"{d1}-{d2}",
                'W': stat,
                'p-value': p,
                'difference_median': (d1_values - d2_values).median()
            })
        #print(f"\nW = {stat}, p = {p}")
    return results

def check_difficulty_significance(dataset, metric):
    conditions = ['EGOCENTRIC', 'EXOCENTRIC']
    difficulties = ['EASY', 'MEDIUM', 'HARD']
    normal = compare_for_normality(dataset, metric)
    results = []
    if normal:
        try:
            anova = AnovaRM(dataset, depvar=metric, subject='UserID',
                            within=['ViewingCondition','Difficulty']).fit()
            print(anova)
        except Exception as e:
            print("Error running ANOVA:", e)
    else:
        for cond in conditions:

            subset = dataset[dataset['ViewingCondition'] == cond]
            pivot = subset.pivot_table(
                index='UserID',
                columns='Difficulty',
                values=metric
            ).dropna()

            values = [pivot[d].values for d in difficulties]
            stat, p = stats.friedmanchisquare(*values)
            #print(f"\n{cond}: Friedman chi2 = {stat:.2f}, p = {p}")
            if (p < 0.05):
                pairwise_results = difficulty_pairwise_wilcoxon(dataset, metric, cond)
                for result in pairwise_results:
                    result['FriedmanChi2'] = stat
                    result['FriedmanP'] = p

                    results.append(result)
            else:
                results.append(
                {
                    'Task': None,
                    'Metric': metric,
                    'ViewingCondition': cond,
                    'FriedmanChi2': stat,
                    'FriedmanP': p,
                    'Difficulty': None,
                    'W': None,
                    'p-value': None
                })
    return results

def compare_viewpoints_difficulties(data, metric):
    #print(f"\nComparing difficulties for {metric}:")

    difficulty_order = ("EASY", "MEDIUM", "HARD")

    pivot = data.pivot_table(
        index=["UserID", "ViewingCondition"],
        columns="Difficulty",
        values=metric
    ).dropna()
    results = []
    for d1, d2 in itertools.combinations(difficulty_order, 2):
        #print(f"\n--- {d1} vs {d2} ---")

        subset = pivot[[d1, d2]].copy()

       
        for condition in ["EGOCENTRIC", "EXOCENTRIC"]:
            cond_data = subset.xs(condition, level="ViewingCondition").dropna()

            stat, p = stats.wilcoxon(cond_data[d1], cond_data[d2])

        subset["diff"] = subset[d2] - subset[d1]

        ego = subset.xs("EGOCENTRIC", level="ViewingCondition")["diff"]
        exo = subset.xs("EXOCENTRIC", level="ViewingCondition")["diff"]

        common = ego.index.intersection(exo.index)
        ego = ego.loc[common]
        exo = exo.loc[common]

        stat, p = stats.wilcoxon(ego, exo)
        results.append(
            {
                'Task': None,
                'Metric': metric,
                'DifficultyComparison': f"{d1} vs {d2}",
                'W': stat,
                'p-value': p,
                'EgoDifference': ego.median(),
                'ExoDifference': exo.median()
            })
        #print(f"DIFF (EGO vs EXO): W = {stat}, p = {p}")
        #print(f"Median DIFF for EGOCENTRIC: {ego.median()}")
        #print(f"Median DIFF for EXOCENTRIC: {exo.median()}")
    return results

def compare_viewpoints(dataset, metric):
    ego = dataset[(metric, 'EGOCENTRIC')]
    exo = dataset[(metric, 'EXOCENTRIC')]
    
    paired = np.column_stack((ego, exo))
    paired = paired[~np.isnan(paired).any(axis=1)]
    
    ego_clean = paired[:, 0]
    exo_clean = paired[:, 1]
    
    diff = ego_clean - exo_clean
    shapiro = stats.shapiro(diff)
        
    if shapiro.pvalue > 0.05:
        test = stats.ttest_rel(ego_clean, exo_clean)
        test_name = 'Paired t-test'
    else:
        test = stats.wilcoxon(ego_clean, exo_clean)
        test_name = 'Wilcoxon signed-rank'
        
    ego_median = np.median(ego_clean)
    exo_median = np.median(exo_clean)
    
    
    if metric == "MeanCompletionTime":
        better = "EGOCENTRIC" if ego_median < exo_median else "EXOCENTRIC"
    else:
        better = "EGOCENTRIC" if ego_median > exo_median else "EXOCENTRIC"
        
    return {
        'Task': None,  
        'Metric': metric,
        'Test': test_name,
        'Statistic': test.statistic,
        'p-value': test.pvalue,
        'Ego_Median': ego_median,
        'Exo_Median': exo_median,
        'Better': better,
        'Shapiro_p': shapiro.pvalue,
    }

def pivot_and_calculate_diff(dataset, metrics):
    pivot = dataset.pivot_table(
        index=['UserID', 'Difficulty'],
        columns='ViewingCondition',
        values=metrics,
        aggfunc='mean'
    )
    
    for metric in metrics:
        pivot[f'{metric}Difference'] = (
            pivot[(metric, 'EGOCENTRIC')] 
            - pivot[(metric, 'EXOCENTRIC')]
        )
    
    return pivot.reset_index()