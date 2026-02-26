import os

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
