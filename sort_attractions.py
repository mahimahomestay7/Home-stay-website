import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update Map iframe
new_iframe = '<iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3929.7042571343714!2d75.9876111!3d12.4359167!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3ba509cae5947365%3A0x4dbc76bc1f7d5511!2sMahima%20Home%20Stay!5e0!3m2!1sen!2sin!4v1700000000000!5m2!1sen!2sin" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>'
iframe_pattern = r'<iframe[^>]*src="https://www.google.com/maps/embed\?[^>]*></iframe>'
content = re.sub(iframe_pattern, new_iframe, content)

# 2. Extract and sort attraction cards
# Find the start and end of attractions grid
grid_start = content.find('<div class="attractions-grid">')
if grid_start != -1:
    grid_end = content.find('</section>', grid_start)
    
    grid_html = content[grid_start:grid_end]
    
    # Extract all attraction cards. We assume each card starts with <div class="attraction-card reveal">
    card_pattern = re.compile(r'<div class="attraction-card reveal">.*?<a class="attraction-link"[^>]*>.*?</a>\s*</div>', re.DOTALL)
    cards = card_pattern.findall(grid_html)
    
    # Parse distance and sort
    def get_dist(card_html):
        # Look for ~X.X km away
        m = re.search(r'~([0-9.]+) km away', card_html)
        if m:
            return float(m.group(1))
        return 999.0 # fallback for 'Coordinates not found' or similar
        
    cards.sort(key=get_dist)
    
    # Rebuild the grid
    new_grid_html = '<div class="attractions-grid">\n    ' + '\n    '.join(cards) + '\n  </div>\n'
    
    # Replace in content
    content = content[:grid_start] + new_grid_html + content[grid_end:]

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated iframe and sorted attractions.")
