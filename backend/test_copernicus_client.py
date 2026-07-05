import os
from dotenv import load_dotenv

load_dotenv()

from app.core.copernicus_client import CopernicusClient

def test():
    client = CopernicusClient()
    # Jorf Lasfar lat, lon
    result = client.fetch_environmental_data(33.103, -6.852)
    print(result)

if __name__ == "__main__":
    test()
