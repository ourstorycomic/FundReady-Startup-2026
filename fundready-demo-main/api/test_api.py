import requests
import json

# Đọc file test
with open('/home/schizo16/Downloads/DEMO-20260727T053112Z-1-001/DEMO/Bao_Cao_Du_Bao_Tai_Chinh_VND.pdf', 'rb') as f:
    files = {'file': ('test.pdf', f, 'application/pdf')}
    data = {'document_type': 'financial'}
    
    response = requests.post(
        'https://fundready-backend.onrender.com/api/upload-document',
        files=files,
        data=data,
        timeout=60
    )
    
    result = response.json()
    print(json.dumps(result, indent=2, ensure_ascii=False))
