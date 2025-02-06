# helpers/determine_trend.py
"""
Determine trend module.
"""


from constants import Trend

CHECK_CURRENT_CANDLE: bool = True
return_value: Trend | None = None

def determine_trend(data_frame, candle) -> Trend:
    """
    This function does something.

    Args:
        data_frame: Description of param1.
        candle: Description of param2.

    Returns:
        Trend direction
    """

    global return_value

    return_value = Trend.NONE

    if data_frame is not None:
        data_frame = data_frame.copy()  # Ensure we are working with a copy

        fractals = data_frame[data_frame['Fractal_Up'].notnull() | data_frame['Fractal_Down'].notnull()][['timestamp', 'Fractal_Down', 'Fractal_Up']]

        fractals_up = fractals[fractals['Fractal_Up'].notnull()]['Fractal_Up']
        fractals_down = fractals[fractals['Fractal_Down'].notnull()]['Fractal_Down']


        if fractals_up.iloc[-1] > fractals_up.iloc[-2] and fractals_down.iloc[-1] > fractals_down.iloc[-2]:
            return_value = Trend.BULLISH
            if CHECK_CURRENT_CANDLE and fractals_down.iloc[-1] > candle['low']:
                return_value = Trend.NONE

        if fractals_up.iloc[-1] < fractals_up.iloc[-2] and fractals_down.iloc[-1] < fractals_down.iloc[-2]:
            return_value = Trend.BEARISH
            if CHECK_CURRENT_CANDLE and fractals_up.iloc[-1] < candle['high']:
                return_value = Trend.NONE

    return return_value


if __name__ == '__main__':
    pass
