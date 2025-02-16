"""
This module provides functions to detect and remove redundant fractals in financial data.
"""


import pandas as pd
import numpy as np


def detect_fractals(data, periods):
    """
    Removes redundant fractals from the given data.

    Args:
        data (pd.DataFrame): The input data containing 'high' and 'low' columns.
        periods (int): The number of periods to consider for detecting fractals.

    Returns:
        pd.DataFrame: The data with redundant fractals removed.
    """
    data['Fractal_Up'] = np.nan
    data['Fractal_Down'] = np.nan

    for i in range(periods, len(data) - periods):
        if data['high'].iloc[i] == max(data['high'].iloc[i - periods:i + periods + 1]):
            data.loc[i, 'Fractal_Up'] = data['high'].iloc[i]
        if data['low'].iloc[i] == min(data['low'].iloc[i - periods:i + periods + 1]):
            data.loc[i, 'Fractal_Down'] = data['low'].iloc[i]
    return data


def remove_redundant_fractals(data, fractal_col, opposite_fractal_col, comparison_op):
    """
    Detects fractals in the given data.

    Args:
        data (pd.DataFrame): The input data containing 'high' and 'low' columns.
        fractal_col (str): The column name of the fractal to detect.
        opposite_fractal_col (str): The column name of the opposite fractal.
        comparison_op (function): The comparison operation to use for detecting redundant fractals.

    Returns:
        pd.DataFrame: The data with detected fractals.
    """
    indices_to_drop = []
    last_fractal_index = None

    for i in range(len(data)):
        if not pd.isnull(data.loc[i, fractal_col]):
            if last_fractal_index is not None:
                is_any_opposite_fractal = not data.loc[
                                              last_fractal_index + 1:i, opposite_fractal_col
                                              ].isnull().all()
                if not is_any_opposite_fractal:
                    if comparison_op(
                            data.loc[last_fractal_index, fractal_col],
                            data.loc[i, fractal_col]
                    ):
                        indices_to_drop.append(i)
                    else:
                        indices_to_drop.append(last_fractal_index)
                        last_fractal_index = i
                else:
                    last_fractal_index = i
            else:
                last_fractal_index = i

    data = data.drop(index=indices_to_drop).reset_index(drop=True)
    return data


def set_fractals(data, periods=24):
    """
    Detects and removes redundant fractals in the given data.

    Args:
        data (pd.DataFrame): The input data containing 'high' and 'low' columns.
        periods (int): The number of periods to consider for detecting fractals.

    Returns:
        pd.DataFrame: The data with detected and cleaned fractals.
    """
    data = data.copy()
    data = detect_fractals(data, periods)
    data = remove_redundant_fractals(data, 'Fractal_Up', 'Fractal_Down', lambda x, y: x >= y)
    data = remove_redundant_fractals(data, 'Fractal_Down', 'Fractal_Up', lambda x, y: x <= y)
    return data


if __name__ == '__main__':
    pass
