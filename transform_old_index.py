#!/usr/bin/env python3
"""
transform_old_index.py

Reads your existing index.html, extracts each <tr class="sheet-row">,
and writes out rows_new.html containing <div class="row">…</div> blocks
in the responsive format.
"""

from bs4 import BeautifulSoup

# Path to your existing index.html
OLD_HTML = 'index.html'
# Output file for converted rows
OUTPUT = 'rows_new.html'

def main():
    # Parse the old HTML
    with open(OLD_HTML, encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    # Select all cheat-sheet rows
    rows = soup.select('tbody tr.sheet-row')
    new_rows = []

    for tr in rows:
        # Get the description text (first <td>)
        desc_td = tr.find('td', class_='chips')
        desc_text = desc_td.get_text(strip=True)

        # Build the steps from the second <td>
        action_td = tr.find_all('td')[1]
        steps = []
        for el in action_td.contents:
            if getattr(el, 'name', None) == 'img':
                src = el['src']
                alt = el.get('alt', '')
                steps.append(f'<div class="step image"><img src="{src}" alt="{alt}" /></div>')
            elif getattr(el, 'name', None) == 'span':
                text = el.get_text(strip=True)
                # Decide if it's a symbol or text
                if text in ['+', '−', '→', '←', '↑', '↓']:
                    steps.append(f'<div class="step symbol">{text}</div>')
                else:
                    steps.append(f'<div class="step text">{text}</div>')

        # Assemble the new row block
        block = [
            '<div class="row">',
            f'  <div class="description">{desc_text}</div>',
            '  <div class="action">'
        ]
        for s in steps:
            block.append(f'    {s}')
        block.append('  </div>')
        block.append('</div>\n')

        new_rows.append('\n'.join(block))

    # Write out all new rows
    with open(OUTPUT, 'w', encoding='utf-8') as out:
        out.write('\n'.join(new_rows))

    print(f"Wrote {len(new_rows)} rows into {OUTPUT}")

if __name__ == '__main__':
    main()


