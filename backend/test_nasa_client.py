import os
from dotenv import load_dotenv

load_dotenv()

from app.core.nasa_client import NasaEarthdataClient

def test():
    client = NasaEarthdataClient()
    # Jorf Lasfar lat, lon
    result = client.fetch_environmental_data(33.103, -6.852)
    print(result)

if __name__ == "__main__":
    test()
