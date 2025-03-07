"""
Moduł zawierający funkcję do serializacji danych do formatu JSON.
"""
import json
import pandas as pd

def serialize_data(data) -> str:
    """
    Serializes data to JSON format.
    :param data:
    :return:
    """
    def default_converter(obj):
        if isinstance(obj, pd.Timestamp):
            return obj.isoformat()  # Konwersja Timestamp do stringa
        return str(obj)  # Konwersja innych nieobsługiwanych typów

    return json.dumps(data, default=default_converter)


if __name__ == '__main__':
    pass
