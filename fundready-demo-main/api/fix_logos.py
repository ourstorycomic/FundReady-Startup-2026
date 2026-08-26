import os

def main():
    base_dir = os.path.dirname(__file__)
    json_path = os.path.join(base_dir, 'data', 'investment_funds.json')
    
    # 1. Update JSON
    with open(json_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    new_content = content.replace('https://logo.clearbit.com/', 'https://www.google.com/s2/favicons?sz=128&domain=')
    
    with open(json_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
        
    print("Updated JSON")
    
    # 2. Update index.html
    html_path = os.path.join(os.path.dirname(base_dir), 'index.html')
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    new_content = content.replace('https://logo.clearbit.com/', 'https://www.google.com/s2/favicons?sz=128&domain=')
    
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
        
    print("Updated HTML")

if __name__ == "__main__":
    main()
