"""
Skrypt uruchamiający serwer API.
"""
if __name__ == '__main__':
    # Uruchomienie serwera komendą:
    # uvicorn script_name:app --reload --host

    from api_server import app

    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
