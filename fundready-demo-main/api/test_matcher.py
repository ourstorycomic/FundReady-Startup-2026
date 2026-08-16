import requests
import json

BASE_URL = "http://localhost:8000"

def test_match_profile():
    print("=== Test Match Profile ===")
    
    test_cases = [
        {
            "name": "AgriTech startup giai đoạn sớm",
            "description": "Chúng tôi là startup nông nghiệp công nghệ cao, mới thành lập 6 tháng, đang phát triển MVP cho giải pháp IoT giám sát cây trồng. Doanh thu chưa có, cần gọi vốn seed 2 tỷ để hoàn thiện sản phẩm."
        },
        {
            "name": "SaaS logistics tăng trưởng",
            "description": "Công ty SaaS về quản lý vận tải, ARR 18 tỷ tăng trưởng 220%/năm. Đã có 180 khách hàng doanh nghiệp, retention rate 95%. Đang gọi Series B để mở rộng sang thị trường Đông Nam Á."
        },
        {
            "name": "HealthTech enterprise hoàn chỉnh",
            "description": "HealthTech enterprise với ARR 85 tỷ, profitability 12%. Kiểm toán Big 4, governance chuẩn public company. Sản phẩm triển khai tại 45 bệnh viện. Sẵn sàng cho IPO hoặc strategic acquisition."
        },
        {
            "name": "SME sản xuất chuyển đổi số",
            "description": "Doanh nghiệp sản xuất thương mại 10 năm, doanh thu 45 tỷ/năm, 120 nhân viên. Đang cần chuyển đổi số để tăng năng suất và mở rộng thị trường. Cần gọi vốn để đầu tư ERP và ecommerce B2B."
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n--- Test {i}: {test_case['name']} ---")
        print(f"Input: {test_case['description'][:100]}...")
        
        try:
            response = requests.post(
                f"{BASE_URL}/api/match-profile",
                json={
                    "description": test_case["description"],
                    "top_n": 3
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                matches = result.get("matches", [])
                
                print(f"\nTop {len(matches)} matches:")
                for j, match in enumerate(matches, 1):
                    print(f"\n{j}. {match['company_name']} (similarity: {match['similarity_score']})")
                    print(f"   Industry: {match['industry']}")
                    print(f"   Stage: {match['stage']}")
                    print(f"   Score: {match['total_score']}/100 - {match['grade']}")
                    print(f"   Summary: {match['summary'][:150]}...")
            else:
                print(f"Error: {response.status_code} - {response.text}")
        
        except Exception as e:
            print(f"Exception: {str(e)}")

def test_analyze_with_reference():
    print("\n\n=== Test Analyze With Reference ===")
    
    description = "Startup nông nghiệp công nghệ cao, mới thành lập, đang phát triển MVP cho giải pháp IoT giám sát cây trồng. Cần gọi vốn seed để hoàn thiện sản phẩm."
    
    print(f"Input: {description}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/analyze-with-reference",
            json={"description": description}
        )
        
        if response.status_code == 200:
            result = response.json()
            
            matched = result.get("matched_profile", {})
            print(f"\nMatched Profile: {matched.get('company_name')}")
            print(f"Similarity: {matched.get('similarity_score')}")
            print(f"Total Score: {matched.get('total_score')}/100")
            
            print(f"\nComparison Note: {result.get('comparison_note')}")
            
            recommendations = result.get("recommendations", [])
            print(f"\nTop Recommendations ({len(recommendations)} total):")
            for rec in recommendations[:3]:
                print(f"  - [{rec.get('priority')}] {rec.get('category')}: {rec.get('recommendation')}")
            
            risks = result.get("risks", [])
            print(f"\nTop Risks ({len(risks)} total):")
            for risk in risks[:3]:
                print(f"  - [{risk.get('severity')}] {risk.get('category')}: {risk.get('financial_impact')}")
        else:
            print(f"Error: {response.status_code} - {response.text}")
    
    except Exception as e:
        print(f"Exception: {str(e)}")

if __name__ == "__main__":
    test_match_profile()
    test_analyze_with_reference()
