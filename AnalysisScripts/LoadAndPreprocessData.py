import pandas as pd
import altair as alt
import numpy as np
from scipy import stats

def filter_data(data):
    return data[(data['UserID']!=6) & (data['TaskPhase']!='training')]

def apply_meta_data(df, meta_data):
    df = df.merge(meta_data, on=["UserID","TaskID"], how='left',validate="m:1")
    return df

def LoadData():
    df_performance = pd.read_csv("Performance.csv")
    df_performance["StartingTime"] = df_performance["TIMESTAMP"] - df_performance["CompletionTime"]
    df_interaction = pd.read_csv("InteractionBehaviour.csv")
    df_movement = pd.read_csv("MovementBehaviour.csv")

    perf_meta = (
        df_performance
        .rename(columns={"UserID":"UserID"})
        .sort_values(["UserID","TaskID","TIMESTAMP"], ascending=[True,True,True])
        .drop_duplicates(subset=["UserID","TaskID"], keep="first")
        [["UserID","TaskID","ViewingCondition","Task","Difficulty","TaskPhase", "StartingTime","CompletionTime"]]
    )

    df_movement = apply_meta_data(df_movement, perf_meta)
    df_interaction = apply_meta_data(df_interaction, perf_meta)

    df_performance = filter_data(df_performance)
    df_interaction = filter_data(df_interaction)
    df_movement = filter_data(df_movement)

    return df_performance, df_interaction, df_movement

def GetPerformanceMeta():
    df_performance = pd.read_csv("RawData/Performance.csv")
    df_performance["StartingTime"] = df_performance["TIMESTAMP"] - df_performance["CompletionTime"]
    perf_meta = (
        df_performance
        .rename(columns={"UserID":"UserID"})
        .sort_values(["UserID","TaskID","TIMESTAMP"], ascending=[True,True,True])
        .drop_duplicates(subset=["UserID","TaskID"], keep="first")
        [["UserID","TaskID","ViewingCondition","Task","Difficulty","TaskPhase", "StartingTime","CompletionTime"]]
    )
    return perf_meta

def LoadPerformanceData():
    df_performance = pd.read_csv("RawData/Performance.csv")
    df_performance["StartingTime"] = df_performance["TIMESTAMP"] - df_performance["CompletionTime"]
    df_performance = filter_data(df_performance)
    return df_performance

def LoadContinuousData(filename):
    df = pd.read_csv(f"RawData/{filename}")
    df = apply_meta_data(df, GetPerformanceMeta())
    df = filter_data(df)
    return df

def LoadInteractionData():
    return LoadContinuousData("InteractionBehaviour.csv")

def LoadMovementData():
    return LoadContinuousData("MovementBehaviour.csv")
