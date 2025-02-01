# helpers/determine_trend.py
"""
Determine trend module.
"""


from constants import Trend


def determine_trend(data_frame) -> Trend:
    """
    This function does something.

    Args:
        data_frame: Description of param1.

    Returns:
        Trend direction
    """


    if data_frame is not None:
        data_frame = data_frame.copy()  # Ensure we are working with a copy

        # data_frame.loc[:, ('ema_50')] = calculate_ema(data_frame['close'], 50)
        # data_frame.loc[:, ('ema_200')] = calculate_ema(data_frame['close'], 200)
        #
        # if data_frame['ema_50'].iloc[-1] > data_frame['ema_200'].iloc[-1]:
        #     return TREND_BULLISH  # Trend wzrostowy
        # if data_frame['ema_50'].iloc[-1] < data_frame['ema_200'].iloc[-1]:
        #     return TREND_BEARISH  # Trend spadkowy


        # # data_frame['RSI'] = talib.RSI(data_frame['close'], timeperiod=14)  # RSI z domyślnym okresem 14
        # # data_frame['MACD'], data_frame['Signal_Line'], _ = talib.MACD(data_frame['close'], fastperiod=12, slowperiod=26, signalperiod=9)
        # # data_frame['MA_50'] = talib.SMA(data_frame['close'], timeperiod=50)
        # # data_frame['MA_200'] = talib.SMA(data_frame['close'], timeperiod=200)
        #
        # row = data_frame.iloc[-1]
        # # pprint.pprint(row)
        # # print(len(data_frame))
        # if (
        #         row['RSI'] <= 50 and  # RSI poniżej 50
        #         row['MACD'] <= row['Signal_Line'] and  # MACD poniżej Signal Line
        #         row['MA_50'] < row['MA_200']  # MA_50 poniżej MA_200
        #     ):
        #     return TREND_BEARISH
        #
        # if (
        #         row['RSI'] > 50 and  # RSI powyżej 50
        #         row['MACD'] > row['Signal_Line'] and  # MACD powyżej Signal Line
        #         row['MA_50'] > row['MA_200']  # MA_50 powyżej MA_200
        #     ):
        #     return TREND_BULLISH

        fractals = data_frame[data_frame['Fractal_Up'].notnull() | data_frame['Fractal_Down'].notnull()][['timestamp', 'Fractal_Down', 'Fractal_Up']]

        fractals_up = fractals[fractals['Fractal_Up'].notnull()]['Fractal_Up']
        fractals_down = fractals[fractals['Fractal_Down'].notnull()]['Fractal_Down']

        # if not np.isnan(fractals['Fractal_Up'].iloc[-1]):
        #     # print(f'Fractal_Up: {fractals['timestamp'].iloc[-1]}, {fractals['Fractal_Up'].iloc[-1]}')
        #     return Trend.BEARISH
        #
        # if not np.isnan(fractals['Fractal_Down'].iloc[-1]):
        #     # print(f'Fractal_Down: {fractals['timestamp'].iloc[-1]}, {fractals['Fractal_Down'].iloc[-1]}')
        #     return Trend.BULLISH

        if fractals_up.iloc[-1] > fractals_up.iloc[-2] and fractals_down.iloc[-1] > fractals_down.iloc[-2]:
            return Trend.BULLISH

        if fractals_up.iloc[-1] < fractals_up.iloc[-2] and fractals_down.iloc[-1] < fractals_down.iloc[-2]:
            return Trend.BEARISH

    return Trend.NONE


if __name__ == '__main__':
    pass
