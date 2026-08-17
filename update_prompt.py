import os

files = ['fundready-demo-main/api/groq_client.py', 'fundready-demo-main/api/gemini_client.py']

replacements = {
    "TỐI THIỂU 100 CHỮ": "CỰC KỲ CHI TIẾT TỐI THIỂU 250 CHỮ",
    "tối thiểu 50 chữ": "cực kỳ chi tiết tối thiểu 150 chữ, trích dẫn số liệu cụ thể",
    "Ít nhất 150 chữ": "Ít nhất 300 chữ, mổ xẻ mọi góc độ",
    "Ít nhất 100 chữ": "Ít nhất 250 chữ, phân tích chuyên sâu",
    "Ít nhất 70 chữ": "Ít nhất 150 chữ",
    "KHÔNG CHUNG CHUNG": "KHÔNG CHUNG CHUNG, VIẾT RẤT DÀI VÀ CỰC KỲ CHI TIẾT",
    "PHẢI ĐẦY ĐỦ VÀ CHI TIẾT": "BẮT BUỘC PHẢI RẤT DÀI, CHI TIẾT VÀ BỔ SUNG TẤT CẢ THÔNG TIN QUAN TRỌNG",
    "max_tokens=4000": "max_tokens=8000"
}

for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
        
    for old, new in replacements.items():
        content = content.replace(old, new)
        
    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)
        
print("Updated prompts to be extremely detailed!")
