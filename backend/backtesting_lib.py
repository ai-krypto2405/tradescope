"""
Helper functions for backtesting strategies
"""
import pandas as pd
import numpy as np


def crossover(series1: pd.Series, series2: pd.Series) -> bool:
    """
    Return True if series1 just crossed above series2
    (series1[-2] < series2[-2] and series1[-1] > series2[-1])
    """
    if len(series1) < 2 or len(series2) < 2:
        return False
    return series1.iloc[-2] < series2.iloc[-2] and series1.iloc[-1] > series2.iloc[-1]


def crossunder(series1: pd.Series, series2: pd.Series) -> bool:
    """
    Return True if series1 just crossed below series2
    """
    if len(series1) < 2 or len(series2) < 2:
        return False
    return series1.iloc[-2] > series2.iloc[-2] and series1.iloc[-1] < series2.iloc[-1]
