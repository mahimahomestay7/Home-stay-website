with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# I need to fix the missing closing </div> for each attraction-card.
# If I look closely, the end of each card currently is:
# </a>
#       </div>
#     <div class="attraction-card reveal">
# I can just replace `</a>\n      </div>\n    <div class="attraction-card`
# with `</a>\n      </div>\n    </div>\n    <div class="attraction-card`
# And for the very last card, replace `</a>\n      </div>\n  </div>\n</section>`
# with `</a>\n      </div>\n    </div>\n  </div>\n</section>`

import re
# Fix the consecutive cards
content = re.sub(r'(<a class="attraction-link"[^>]*>.*?</a>\s*</div>)(\s*)<div class="attraction-card', r'\1\n    </div>\2<div class="attraction-card', content)
# Fix the very last card
content = re.sub(r'(<a class="attraction-link"[^>]*>.*?</a>\s*</div>)(\s*)</div>\n</section>', r'\1\n    </div>\2</div>\n</section>', content)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Fixed layout!")
