import os

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace the cache directory creation logic
    old_str = "cache_dir = os.path.join(os.path.dirname(__file__), 'cache')"
    new_str = "cache_dir = '/tmp/cache' if os.environ.get('VERCEL') else os.path.join(os.path.dirname(__file__), 'cache')"
    
    new_content = content.replace(old_str, new_str)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

fix_file('fundready-demo-main/api/groq_client.py')
fix_file('fundready-demo-main/api/gemini_client.py')
print('Fixed cache paths!')
