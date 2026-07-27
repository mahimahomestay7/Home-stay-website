import urllib.request
import json
import time
import ssl
import urllib.parse

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

homestay_coords = "75.987523,12.435747" # lon, lat

places = [
    "Namdroling Golden Temple",
    "Fish Lake 2nd Camp Bylakuppe",
    "Kaveri Nisargadhama",
    "Nisargadhama Bird Park",
    "Coorg Hanging Bridge",
    "Abbey Falls",
    "Raja's Seat",
    "Dubare Elephant Camp",
    "Mandalpatti Peak",
    "Talakaveri",
    "Iruppu Falls",
    "Madikeri Fort",
    "Mallalli Falls",
    "Chiklihole Reservoir",
    "Harangi Dam",
    "Honnamana Kere Lake",
    "Omkareswara Temple",
    "Kotebetta Peak",
    "Nalknad Aramane Palace",
    "Nehru Mantap",
    "Padi Iggutappa Temple",
    "Somwarpet",
    "Suntikoppa",
    "Tadiandamol Trek"
]

results = {}
for place in places:
    query = urllib.parse.quote(place + " Karnataka")
    url = f"https://nominatim.openstreetmap.org/search?q={query}&format=json&limit=1"
    req = urllib.request.Request(url, headers={'User-Agent': 'MahimaHomestayApp/1.0 (mahimahomestay7@gmail.com)'})
    try:
        with urllib.request.urlopen(req, context=ctx) as response:
            data = json.loads(response.read().decode())
            if data:
                lat = data[0]['lat']
                lon = data[0]['lon']
                
                route_url = f"http://router.project-osrm.org/route/v1/driving/{homestay_coords};{lon},{lat}?overview=false"
                with urllib.request.urlopen(route_url) as r_response:
                    r_data = json.loads(r_response.read().decode())
                    if r_data.get('routes'):
                        dist_km = r_data['routes'][0]['distance'] / 1000
                        results[place] = round(dist_km, 1)
                        print(f"{place}: {dist_km:.1f} km")
                    else:
                        print(f"{place}: Route not found")
            else:
                print(f"{place}: Coordinates not found")
    except Exception as e:
        print(f"{place}: Error {e}")
    time.sleep(1)

with open('dists.json', 'w') as f:
    json.dump(results, f)
