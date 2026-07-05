import os
import sys
from pprint import pprint
from app.core.nasa_client import NasaEarthdataClient
from app.core.copernicus_client import CopernicusClient

# Coordinates for Jorf Lasfar
LAT = 33.1039
LON = -8.6253

def main():
    print("=== Testing Real Environmental Data Pipelines ===")
    
    print("\n1. Testing Copernicus Client (Rasterio / NDWI Extraction)")
    try:
        copernicus_client = CopernicusClient()
        copernicus_res = copernicus_client.fetch_environmental_data(LAT, LON)
        if "error" in copernicus_res:
            print(f"Copernicus Error: {copernicus_res['error']}")
        else:
            print("Copernicus Data successfully extracted using Rasterio MemoryFile:")
            pprint(copernicus_res['payload'])
            print(f"Product: {copernicus_res['metadata']['product']}")
    except Exception as e:
        print(f"Copernicus pipeline failed: {e}")

    print("\n2. Testing NASA Client (Xarray / NetCDF Extraction)")
    try:
        nasa_client = NasaEarthdataClient()
        nasa_res = nasa_client.fetch_environmental_data(LAT, LON)
        if "error" in nasa_res:
            print(f"NASA Error: {nasa_res['error']}")
        else:
            print("NASA Data successfully extracted using Xarray CF Convention Generator:")
            pprint(nasa_res['payload'])
            print(f"Granule: {nasa_res['metadata']['granule']}")
    except Exception as e:
        print(f"NASA pipeline failed: {e}")

if __name__ == "__main__":
    # Add project root to sys.path
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    main()
