import os
import shutil
import re

mapping = {
    "Fish Lake (2nd Camp Lake)": "/Users/arun_v/.gemini/antigravity/brain/fcd1495c-162b-4509-ac31-4c3346e0e849/fish_lake_1784130175156.jpg",
    "Coorg Hanging Bridge": "/Users/arun_v/.gemini/antigravity/brain/fcd1495c-162b-4509-ac31-4c3346e0e849/hanging_bridge_1784130188316.jpg",
    "Mandalpatti Peak": "/Users/arun_v/.gemini/antigravity/brain/fcd1495c-162b-4509-ac31-4c3346e0e849/mandalpatti_peak_1784130200764.jpg",
    "Chiklihole Reservoir": "/Users/arun_v/.gemini/antigravity/brain/fcd1495c-162b-4509-ac31-4c3346e0e849/chiklihole_1784130212158.jpg",
    "Nehru Mantap": "/Users/arun_v/.gemini/antigravity/brain/fcd1495c-162b-4509-ac31-4c3346e0e849/nehru_mantap_1784130239453.jpg",
    "Padi Iggutappa Temple": "/Users/arun_v/.gemini/antigravity/brain/fcd1495c-162b-4509-ac31-4c3346e0e849/padi_iggutappa_1784130251214.jpg",
    "Tadiandamol Trek": "/Users/arun_v/.gemini/antigravity/brain/fcd1495c-162b-4509-ac31-4c3346e0e849/tadiandamol_1784130263975.jpg"
}

img_dir = "attractions_images"
os.makedirs(img_dir, exist_ok=True)

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

for name, src_path in mapping.items():
    safe_name = re.sub(r'[^a-zA-Z0-9]', '_', name) + ".jpg"
    dest_path = os.path.join(img_dir, safe_name)
    
    # Copy the file
    shutil.copy(src_path, dest_path)
    print(f"Copied {src_path} to {dest_path}")
    
    # Replace in index.html
    # We find `<img class="attraction-img" src="..." alt="name"`
    pattern = rf'(<img class="attraction-img" src=")[^"]+(" alt="{re.escape(name)}")'
    content = re.sub(pattern, rf'\g<1>{dest_path}\g<2>', content)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Finished updating remaining images!")
