import os
import re

def modularize_html():
    os.makedirs('components', exist_ok=True)
    
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
        
    # We will identify sections by semantic tags and comments
    sections = [
        ('navbar', r'<nav class="navbar">.*?</nav>'),
        ('hero', r'<header class="hero">.*?</header>'),
        ('services', r'<!-- ================= SERVICIOS ================= -->.*?</section>'),
        ('testimonials', r'<section\s+id="testimonios".*?</section>'),
        ('pricing', r'<section id="precios".*?</section>'),
        ('maintenance', r'<!-- ================= MANTENIMIENTO BOX ================= -->.*?</div>\s+</div>'),
        ('contact', r'<!-- ================= CONTACTO \(NUEVO\) ================= -->.*?</section>'),
        ('footer', r'<footer.*?</script>')
    ]
    
    template = content
    
    for name, pattern in sections:
        match = re.search(pattern, content, flags=re.DOTALL)
        if match:
            section_content = match.group(0)
            
            # Save component
            with open(f'components/{name}.html', 'w', encoding='utf-8') as f:
                f.write(section_content)
                
            # Replace in template with placeholder
            template = template.replace(section_content, f'<!-- INCLUDE components/{name}.html -->')
        else:
            print(f"Warning: Could not find section '{name}'")
            
    # Save the base template
    os.rename('index.html', 'index.html.bak')
    with open('index.template.html', 'w', encoding='utf-8') as f:
        f.write(template)
        
    print("HTML accurately split into components/ directory.")
    print("Created index.template.html.")

    # Create the builder script
    builder_code = """import os

def build():
    with open('index.template.html', 'r', encoding='utf-8') as f:
        template = f.read()
        
    import re
    def replace_include(match):
        filename = match.group(1)
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as cf:
                return cf.read()
        else:
            print(f"Warning: Component {filename} not found.")
            return match.group(0)
            
    final_html = re.sub(r'<!-- INCLUDE (components/.*?.html) -->', replace_include, template)
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(final_html)
        
    print("Successfully built index.html from components!")

if __name__ == '__main__':
    build()
"""
    with open('build_html.py', 'w', encoding='utf-8') as f:
        f.write(builder_code)
        
    print("Created build_html.py to reconstruct index.html.")

if __name__ == '__main__':
    modularize_html()
