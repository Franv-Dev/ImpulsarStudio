import os
import re

def modularize():
    # Read CSS
    with open('styles.css', 'r', encoding='utf-8') as f:
        css_content = f.read()

    # Define CSS modules to extract mapping headers to filenames
    modules = [
        ("reset", "/* ================= RESET ================= */"),
        ("hero", "/* ================= HERO ================= */"),
        ("services", "/* ================= SERVICIOS ================= */"),
        ("footer", "/* ================= FOOTER ================= */"),
        ("testimonials", "/* ================= TESTIMONIOS (MARQUEE EFFECT) ================= */"),
        ("pricing", "/* ================= PRECIOS CSS ================= */"),
        ("maintenance", "ESTILOS DE MANTENIMIENTO (NUEVO)"),
        ("glow", "/* ================= SPOTLIGHT CARD EFFECT ================= */"),
        ("contact", "CONTACTO (NUEVO)"),
        ("animations", "ANIMACIONES DE ENTRADA (NUEVO)")
    ]

    indexes = []
    for name, marker in modules:
        idx = css_content.find(marker)
        if idx != -1:
            # We want to find the exact line where this comment starts.
            # Usually we just take the nearest '/*' before it.
            comment_start = css_content.rfind('/*', 0, idx)
            if comment_start != -1 and comment_start >= css_content.rfind('}', 0, idx):
                idx = comment_start
            indexes.append((idx, name))
        else:
            print(f"Warning: Marker for {name} not found.")

    indexes.sort(key=lambda x: x[0])

    # Ensure css folder exists
    os.makedirs('css', exist_ok=True)

    # Split and write CSS files
    css_links = ""
    for i, (idx, name) in enumerate(indexes):
        start = idx
        if i < len(indexes) - 1:
            end = indexes[i+1][0]
            content = css_content[start:end]
        else:
            content = css_content[start:]
        
        with open(f'css/{name}.css', 'w', encoding='utf-8') as f:
            f.write(content.strip() + '\n')
        css_links += f'    <link rel="stylesheet" href="css/{name}.css" />\n'

    # Read HTML
    with open('index.html', 'r', encoding='utf-8') as f:
        html_content = f.read()

    # Replace <link rel="stylesheet" href="styles.css" /> with all the new links
    if 'href="styles.css"' in html_content:
        html_content = re.sub(r' *<link rel="stylesheet" href="styles.css" />\n?', css_links, html_content)
    else:
        print("Warning: styles.css link not found in index.html.")

    # Extract JS
    os.makedirs('js', exist_ok=True)
    # Find all script tags
    scripts = re.findall(r'<script>(.*?)</script>', html_content, flags=re.DOTALL)
    if scripts:
        # Assuming the last script is our main JS
        js_content = scripts[-1].strip()
        with open('js/main.js', 'w', encoding='utf-8') as f:
            f.write(js_content + '\n')
        
        # Replace the literal script block
        old_script_block = f"<script>{scripts[-1]}</script>"
        html_content = html_content.replace(old_script_block, '<script src="js/main.js"></script>')

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)

    os.rename('styles.css', 'styles.css.bak')
    print("Modularization complete!")

if __name__ == "__main__":
    modularize()
