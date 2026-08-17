import os
from pathlib import Path

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    old_str = 'CACHE_DIR = Path(__file__).parent / "cache"\nCACHE_DIR.mkdir(exist_ok=True)'
    new_str = '''if os.environ.get('VERCEL'):
    CACHE_DIR = Path('/tmp/cache')
else:
    CACHE_DIR = Path(__file__).parent / "cache"

try:
    CACHE_DIR.mkdir(exist_ok=True)
except OSError:
    pass'''
    
    if old_str in content:
        new_content = content.replace(old_str, new_str)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f'Fixed {filepath}')
    else:
        print(f'Pattern not found in {filepath}')

fix_file('fundready-demo-main/api/groq_client.py')
fix_file('fundready-demo-main/api/file_parser.py')

def fix_gemini():
    filepath = 'fundready-demo-main/api/gemini_client.py'
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    old_str = "cache_dir = os.path.join(os.path.dirname(__file__), 'cache')\n        if not os.path.exists(cache_dir):\n            os.makedirs(cache_dir)"
    new_str = '''cache_dir = '/tmp/cache' if os.environ.get('VERCEL') else os.path.join(os.path.dirname(__file__), 'cache')
        try:
            if not os.path.exists(cache_dir):
                os.makedirs(cache_dir)
        except OSError:
            pass'''
            
    if old_str in content:
        new_content = content.replace(old_str, new_str)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f'Fixed gemini_client.py')

fix_gemini()
