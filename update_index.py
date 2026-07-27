import os
import re
import json
import urllib.request
import ssl
import time

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

with open('dists.json', 'r', encoding='utf-8') as f:
    dists = json.load(f)

imgs = {
    "Namdroling Golden Temple": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/15/Namdroling_Monastery_Golden_Temple_2022_%2825%29.jpg/800px-Namdroling_Monastery_Golden_Temple_2022_%2825%29.jpg",
    "Fish Lake (2nd Camp Lake)": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/cd/Bylakuppe_Fish_Lake.jpg/800px-Bylakuppe_Fish_Lake.jpg",
    "Kaveri Nisargadhama": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/87/Kaveri_Nisargadhama.JPG/800px-Kaveri_Nisargadhama.JPG",
    "Nisargadhama Bird Park": "https://lh3.googleusercontent.com/places/ANXAkqF-UKqll28PJENhGykdBL8CvS__EmFOEN9SQ2f6XBaViEV1IVyVvaXmYO5cSPj2q5bZZ-65HmpxpT3MgCsCC611pP4MsdctNoA=s800-w576-h324",
    "Coorg Hanging Bridge": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f7/Hanging_bridge_at_Cauvery_Nisargadhama.jpg/800px-Hanging_bridge_at_Cauvery_Nisargadhama.jpg",
    "Abbey Falls": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7a/Abbey_Falls_New.jpg/800px-Abbey_Falls_New.jpg",
    "Raja's Seat": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c6/Raja_seat_madikeri.JPG/800px-Raja_seat_madikeri.JPG",
    "Dubare Elephant Camp": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/97/Kaveri_by_Dubare_Forest.jpg/800px-Kaveri_by_Dubare_Forest.jpg",
    "Mandalpatti Peak": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Mandalpatti_Peak_Coorg.jpg/800px-Mandalpatti_Peak_Coorg.jpg",
    "Talakaveri (Talacauvery)": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Talakaveri.jpg/800px-Talakaveri.jpg",
    "Iruppu Falls": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/86/Iruppu_Waterfalls.jpg/800px-Iruppu_Waterfalls.jpg",
    "Madikeri Fort": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c8/Madikeri_Palace_now_used_as_district_administration_seat.jpg/800px-Madikeri_Palace_now_used_as_district_administration_seat.jpg",
    "Mallalli Falls": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1e/Mallalli_falls_1.jpg/800px-Mallalli_falls_1.jpg",
    "Chiklihole Reservoir": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/29/Chiklihole_Reservoir.jpg/800px-Chiklihole_Reservoir.jpg",
    "Harangi Dam": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/07/Harangi_Dam.jpg/800px-Harangi_Dam.jpg",
    "Honnamana Kere Lake": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e6/Honnamana_Kere.jpg/800px-Honnamana_Kere.jpg",
    "Omkareswara Temple": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3d/Omkareshwara_Temple.jpg/800px-Omkareshwara_Temple.jpg",
    "Kotebetta Peak": "https://www.holidify.com/images/cmsuploads/compressed/photo-1467139701929-18c0d27a7516_20191014185312.jpg",
    "Nalknad Aramane Palace": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/36/Nalknad_Palace.jpg/800px-Nalknad_Palace.jpg",
    "Nehru Mantap": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Sunset_at_Madikeri.jpg/800px-Sunset_at_Madikeri.jpg",
    "Padi Iggutappa Temple": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0b/Padi_Iggutappa_Temple.jpg/800px-Padi_Iggutappa_Temple.jpg",
    "Somwarpet": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/87/Somwarpet_coorg.jpg/800px-Somwarpet_coorg.jpg",
    "Suntikoppa": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/ca/Nakoor_Volkot_Suntikoppa_Coorg_Apr24_A7C_10727.jpg/800px-Nakoor_Volkot_Suntikoppa_Coorg_Apr24_A7C_10727.jpg",
    "Tadiandamol Trek": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7b/Tadiandamol_Peak.jpg/800px-Tadiandamol_Peak.jpg"
}

name_map = {
    "Fish Lake 2nd Camp Bylakuppe": "Fish Lake (2nd Camp Lake)",
    "Talakaveri": "Talakaveri (Talacauvery)"
}

img_dir = "attractions_images"
os.makedirs(img_dir, exist_ok=True)

local_imgs = {}
for name, url in imgs.items():
    safe_name = re.sub(r'[^a-zA-Z0-9]', '_', name) + ".jpg"
    filepath = os.path.join(img_dir, safe_name)
    if not os.path.exists(filepath):
        if "wikimedia.org" in url and "/thumb/" in url:
            m = re.search(r'/thumb/[^/]+/[^/]+/([^/]+)/', url)
            if m:
                special_url = f"https://commons.wikimedia.org/wiki/Special:FilePath/{m.group(1)}"
        else:
            special_url = url
            
        success = False
        for current_url in [special_url, url]:
            if success: break
            req = urllib.request.Request(current_url, headers={'User-Agent': 'MahimaHomestayApp/1.0 (mahimahomestay7@gmail.com)'})
            for attempt in range(2):
                try:
                    with urllib.request.urlopen(req, context=ctx) as response:
                        with open(filepath, 'wb') as f:
                            f.write(response.read())
                    print(f"Downloaded {name} using {current_url}")
                    success = True
                    break
                except Exception as e:
                    print(f"Failed to download {name} via {current_url}: {e}")
                    time.sleep(2)
        if not success:
            continue
    local_imgs[name] = filepath

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

for name, dist in dists.items():
    target_name = name_map.get(name, name)
    pattern = rf'(<h4>{re.escape(target_name)}</h4>.*?<span class="attraction-dist">📍 )~[0-9.]+ km away(</span>)'
    content = re.sub(pattern, rf'\g<1>~{dist} km away\g<2>', content, flags=re.DOTALL)

for name, local_path in local_imgs.items():
    pattern = rf'(<img class="attraction-img" src=")[^"]+(" alt="{re.escape(name)}")'
    content = re.sub(pattern, rf'\g<1>{local_path}\g<2>', content)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("All missing images downloaded and HTML updated!")
