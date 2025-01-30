import pandas as pd
import numpy as np

# Funkcja do obliczania fraktali
def set_fractals(data, periods=24):
    """
    Oblicza fraktale dla zadanego DataFrame.

    Parametry:
    - data: DataFrame, który musi zawierać kolumny 'high' i 'low'.
    - periods: liczba świec przed i po bieżącej, które są brane pod uwagę przy wykrywaniu fraktali.

    Zwraca:
    - DataFrame z dodanymi kolumnami 'Fractal_Up' i 'Fractal_Down'.
    """

    data = data.copy()  # Zapewnienie, że pracujemy na kopii

    # Dodanie kolumn na fraktale
    data['Fractal_Up'] = np.nan
    data['Fractal_Down'] = np.nan

    # Iteracja po DataFrame, z uwzględnieniem marginesów dla n świec
    for i in range(periods, len(data) - periods):
        # Sprawdzenie fraktala górnego (bearish fractal)
        if data['high'].iloc[i] == max(data['high'].iloc[i - periods:i + periods + 1]):
            data.loc[i, 'Fractal_Up'] = data['high'].iloc[i]

        # Sprawdzenie fraktala dolnego (bullish fractal)
        if data['low'].iloc[i] == min(data['low'].iloc[i - periods:i + periods + 1]):
            data.loc[i, 'Fractal_Down'] = data['low'].iloc[i]


    # Iteracyjne usuwanie nadmiarowych Fractal_Up
    # Lista indeksów do usunięcia
    indices_to_drop = []

    # Ostatni zachowany Fractal_Up
    last_fractal_up_index = None

    for i in range(len(data)):
        # Jeśli bieżący wiersz ma Fractal_Up
        if not pd.isnull(data.loc[i, 'Fractal_Up']):
            if last_fractal_up_index is not None:
                # Sprawdź, czy pomiędzy ostatnim Fractal_Up a bieżącym nie ma Fractal_Down
                is_any_fractal_down = not data.loc[last_fractal_up_index + 1:i, 'Fractal_Down'].isnull().all()

                if not is_any_fractal_down:  # Jeśli nie ma Fractal_Down między nimi
                    # Porównaj wartości Fractal_Up
                    if data.loc[last_fractal_up_index, 'Fractal_Up'] >= data.loc[i, 'Fractal_Up']:
                        indices_to_drop.append(i)  # Usuń bieżący
                    else:
                        indices_to_drop.append(last_fractal_up_index)  # Usuń poprzedni
                        last_fractal_up_index = i  # Zaktualizuj wskaźnik
                else:
                    # Jeśli występuje Fractal_Down, zaktualizuj wskaźnik
                    last_fractal_up_index = i
            else:
                # Jeśli to pierwszy Fractal_Up, zapisz jego indeks
                last_fractal_up_index = i

    # Usuń oznaczone wiersze
    data = data.drop(index=indices_to_drop).reset_index(drop=True)


    # Iteracyjne usuwanie nadmiarowych Fractal_Down
    # Lista indeksów do usunięcia
    indices_to_drop = []

    # Ostatni zachowany Fractal_Down
    last_fractal_down_index = None

    for i in range(len(data)):
        # Jeśli bieżący wiersz ma Fractal_Down
        if not pd.isnull(data.loc[i, 'Fractal_Down']):
            if last_fractal_down_index is not None:
                # Sprawdź, czy pomiędzy ostatnim Fractal_Down a bieżącym nie ma Fractal_Up
                is_any_fractal_up = not data.loc[last_fractal_down_index + 1:i, 'Fractal_Up'].isnull().all()

                if not is_any_fractal_up:  # Jeśli nie ma Fractal_Up między nimi
                    # Porównaj wartości Fractal_Down
                    if data.loc[last_fractal_down_index, 'Fractal_Down'] <= data.loc[i, 'Fractal_Down']:
                        indices_to_drop.append(i)  # Usuń bieżący
                    else:
                        indices_to_drop.append(last_fractal_down_index)  # Usuń poprzedni
                        last_fractal_down_index = i  # Zaktualizuj wskaźnik
                else:
                    # Jeśli występuje Fractal_Up, zaktualizuj wskaźnik
                    last_fractal_down_index = i
            else:
                # Jeśli to pierwszy Fractal_Down, zapisz jego indeks
                last_fractal_down_index = i

    # Usuń oznaczone wiersze
    data = data.drop(index=indices_to_drop).reset_index(drop=True)


    # print(data[data['Fractal_Up'].notnull() | data['Fractal_Down'].notnull()][['timestamp', 'Fractal_Down', 'Fractal_Up']])


    return data


if __name__ == '__main__':
    pass
