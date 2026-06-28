def fetch_nasa_power_data(lat: float, lon: float, start_date: str, end_date: str) -> dict:
    """
    Stub for NASA POWER API client.
    Returns simulated environmental time series data.
    """
    return {
        "status": "success",
        "simulated": True,
        "data": {
            "temperature": [],
            "humidity": [],
            "precipitation": []
        }
    }
