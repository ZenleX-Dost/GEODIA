import requests

# The token provided by the user
TOKEN = "eyJ0eXAiOiJKV1QiLCJvcmlnaW4iOiJFYXJ0aGRhdGEgTG9naW4iLCJzaWciOiJlZGxqd3RwdWJrZXlfb3BzIiwiYWxnIjoiUlMyNTYifQ.eyJ0eXBlIjoiVXNlciIsInVpZCI6InplbmxleCIsImV4cCI6MTc4Nzg2MDA1NiwiaWF0IjoxNzgyNjc2MDU2LCJpc3MiOiJodHRwczovL3Vycy5lYXJ0aGRhdGEubmFzYS5nb3YiLCJpZGVudGl0eV9wcm92aWRlciI6ImVkbF9vcHMiLCJhY3IiOiJlZGwiLCJhc3N1cmFuY2VfbGV2ZWwiOjN9.iIfGmgAD7CNOUULJqfQgm9ycvghsjtV-9zP1ndGlf7vZGx3x4KlMY5VSQZXAQt4atNJ5oGY-815gGo81ATc1bTbXK6f3uLC_-8IbdSjnyGa_TK11acmFAge74Nyh86y4Ec70lAzrsHDoz2QdSdi3-w9msxw3WSP702tHitv5BSdzcMfyEQx3uaxfe77RhWA68--bKBQYa7dC3X1V9lHIxhybEh1ulAfriqT1_SAyTaOplehiOFAqjw31_aCgFY7SBwa_vIVWoaAz58l-lb4VfL5_-up67mVhrPbeEQoWrA5fJzGw6EUG07XU3I7oU_ZnZrKoQk1lGRHscnU8U8HV5g"

def test_cmr():
    url = "https://cmr.earthdata.nasa.gov/search/granules.json"
    headers = {
        "Authorization": f"Bearer {TOKEN}"
    }
    # Jorf Lasfar is around Lat 33.103, Lon -6.852
    # Searching for a small bounding box
    params = {
        "bounding_box": "-6.9,33.0,-6.8,33.2",
        "page_size": 2,
        "short_name": "MUR-JPL-L4-GLOB-v4.1",
        "temporal": "2024-01-01T00:00:00Z,"
    }
    
    response = requests.get(url, headers=headers, params=params)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        entries = data.get("feed", {}).get("entry", [])
        print(f"Found {len(entries)} granules.")
        if entries:
            print("First granule:")
            print(entries[0].get("title"))
            print(entries[0].get("time_start"))
    else:
        print(response.text)

if __name__ == "__main__":
    test_cmr()
