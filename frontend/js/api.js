const API_BASE = "http://localhost:8001";

// Mock data strictly for visual demonstration of the premium UI
const mockFullData = {
    "score": {
        "total": 34, "maximum": 100, "grade": "Seed - Chưa đủ điều kiện gọi vốn VC",
        "breakdown": [
            { "name": "Cấu trúc vốn", "score": 8, "maximum": 20, "reason": "Chưa có Cap Table chính thức. Thiếu ESOP." },
            { "name": "Tình hình Tài chính", "score": 6, "maximum": 20, "reason": "Doanh thu thử nghiệm thấp, chưa có BCTC kiểm toán." },
            { "name": "Dòng tiền", "score": 5, "maximum": 15, "reason": "Burn rate cao, runway còn 5 tháng." },
            { "name": "Quản trị", "score": 5, "maximum": 15, "reason": "Chưa có cơ cấu quản trị, chưa ký hợp đồng cổ đông." },
            { "name": "Pháp lý", "score": 6, "maximum": 15, "reason": "Vẫn là hộ kinh doanh cá nhân, chưa lên công ty." },
            { "name": "Định giá", "score": 4, "maximum": 15, "reason": "Định giá cảm tính, thiếu mô hình DCF." }
        ]
    },
    "analysis": {
        "financial_position": "Giai đoạn pre-revenue với doanh thu thử nghiệm rất nhỏ (15 triệu/tháng). Chi phí chủ yếu cho phát triển sản phẩm.",
        "governance": "Quản trị informal giữa các founders, chưa có hợp đồng cổ đông hay vesting schedule.",
        "legal_compliance": "Hoạt động dưới dạng hộ kinh doanh, không đủ điều kiện pháp lý nhận vốn quỹ (VC).",
        "valuation": "Định giá chủ quan dựa trên traction ban đầu (200 khách hàng), chưa có phương pháp định giá chuẩn mực."
    },
    "recommendations": [
        { "priority": "Critical", "recommendation": "Chuyển đổi pháp nhân", "financial_impact": "Từ Hộ kinh doanh sang Công ty Cổ phần để có thể phát hành cổ phần." },
        { "priority": "Critical", "recommendation": "Ký thỏa thuận Cổ đông (SHA)", "financial_impact": "Ràng buộc vesting 4 năm để tránh rủi ro founder rời đi sớm." },
        { "priority": "High", "recommendation": "Chuẩn hóa Kế toán", "financial_impact": "Sử dụng phần mềm kế toán chuẩn bị cho báo cáo minh bạch." }
    ]
};

async function handleAnalyze() {
    const descInput = document.getElementById('descInput');
    const desc = descInput ? descInput.value.trim() : '';
    
    if (!desc) {
        // Optional: show a clean inline error instead of alert
        alert("Vui lòng nhập mô tả doanh nghiệp.");
        return;
    }

    const btn = document.getElementById('analyzeBtn');
    const btnText = document.getElementById('btnText');
    const spinner = document.getElementById('btnSpinner');
    const resultSec = document.getElementById('resultSection');
    const errorBox = document.getElementById('errorBox');
    
    // UI State: Loading
    btn.disabled = true;
    btn.style.opacity = '0.8';
    btnText.textContent = 'Đang phân tích...';
    spinner.classList.remove('hidden');
    if (errorBox) errorBox.classList.add('hidden');
    if (resultSec) resultSec.classList.add('hidden');

    try {
        const response = await fetch(`${API_BASE}/api/analyze-document`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ document_type: "pitchdeck", content: desc })
        });

        if (!response.ok) throw new Error("Server error " + response.status);
        
        const data = await response.json();
        renderResults(data);
    } catch (error) {
        if (errorBox) {
            errorBox.textContent = `Lỗi kết nối: ${error.message}`;
            errorBox.classList.remove('hidden');
        } else {
            console.error(error);
            alert(`Lỗi kết nối: ${error.message}`);
        }
    } finally {
        // UI State: Reset
        btn.disabled = false;
        btn.style.opacity = '1';
        btnText.textContent = 'Phân tích tài liệu';
        spinner.classList.add('hidden');
    }
}

function renderResults(data) {
    const resultSec = document.getElementById('resultSection');
    
    // 1. Top Metrics
    document.getElementById('resScore').textContent = `${data.score || 0}/100`;
    document.getElementById('resTier').textContent = data.grade || 'N/A';
    document.getElementById('resSim').textContent = `AI Phân tích`;
    document.getElementById('resSummary').textContent = "Đánh giá chi tiết từ AI dựa trên Bộ Tiêu Chí doanh nghiệp.";

    // 2. Breakdown
    const breakdown = data.breakdown || [];
    const tbody = document.getElementById('scoreBreakdownBody');
    tbody.innerHTML = '';
    
    breakdown.forEach((b, index) => {
        const pct = (b.score / b.maximum) * 100;
        let colorClass = 'bg-[#4F46E5]'; // Primary Indigo
        if (pct < 40) colorClass = 'bg-[#EF4444]'; // Red
        else if (pct < 70) colorClass = 'bg-[#F59E0B]'; // Amber

        tbody.innerHTML += `
            <tr class="border-b border-gray-100 last:border-0">
                <td class="py-4 px-4 align-top w-1/4">
                    <p class="font-semibold text-gray-900">${b.name}</p>
                </td>
                <td class="py-4 px-4 align-top w-1/3">
                    <div class="flex items-center gap-3">
                        <span class="text-sm font-bold text-gray-700 w-12">${b.score}/${b.maximum}</span>
                        <div class="w-full bg-gray-100 rounded-full h-1.5 overflow-hidden">
                            <div class="${colorClass} h-1.5 rounded-full progress-fill-anim" style="width: ${pct}%"></div>
                        </div>
                    </div>
                </td>
                <td class="py-4 px-4 align-top">
                    <p class="text-sm text-gray-600">${b.reason}</p>
                </td>
            </tr>
        `;
    });

    // 3. Strengths and Weaknesses
    const strengthsList = document.getElementById('strengthsList');
    const weaknessesList = document.getElementById('weaknessesList');
    if (strengthsList) {
        strengthsList.innerHTML = (data.strengths || []).map(s => `<li>${s}</li>`).join('');
    }
    if (weaknessesList) {
        weaknessesList.innerHTML = (data.weaknesses || []).map(w => `<li>${w}</li>`).join('');
    }

    // 4. Funding Scenario
    if (data.funding_scenario) {
        document.getElementById('fsContainer').classList.remove('hidden');
        const fs = data.funding_scenario;
        document.getElementById('fsCurrentDesire').textContent = fs.current_desire || '-';
        if (fs.recommendation) {
            document.getElementById('fsDesired').textContent = fs.recommendation.desired_amount || '-';
            document.getElementById('fsRecommended').textContent = fs.recommendation.recommended_amount || '-';
            document.getElementById('fsDifference').textContent = fs.recommendation.difference || '-';
            document.getElementById('fsRationale').textContent = fs.recommendation.rationale || '-';
        }
        
        const scenariosContainer = document.getElementById('fsScenariosContainer');
        if (scenariosContainer && fs.scenarios) {
            scenariosContainer.innerHTML = fs.scenarios.map((scenario, index) => {
                const allocationHtml = (scenario.allocation || []).map(a => `
                    <tr class="border-b border-gray-100 last:border-0 hover:bg-brand-50/30 transition-colors">
                        <td class="py-3 px-4 font-medium text-gray-900">${a.category}</td>
                        <td class="py-3 px-4 text-center">
                            <span class="badge badge-indigo">${a.percentage}</span>
                        </td>
                        <td class="py-3 px-4 text-right font-semibold text-gray-700">${a.amount}</td>
                        <td class="py-3 px-4 text-sm text-gray-600">${a.objective}</td>
                    </tr>
                `).join('');

                return `
                    <div class="border border-gray-100 rounded-lg overflow-hidden">
                        <div class="bg-gray-50 px-4 py-3 border-b border-gray-100">
                            <h5 class="font-bold text-gray-900 text-sm">3.${index+1} ${scenario.name}</h5>
                        </div>
                        <div class="overflow-x-auto">
                            <table class="w-full text-sm text-left">
                                <thead class="bg-white text-gray-500 text-xs border-b border-gray-100 uppercase">
                                    <tr>
                                        <th class="py-3 px-4">Hạng mục</th>
                                        <th class="py-3 px-4 text-center">Tỷ lệ</th>
                                        <th class="py-3 px-4 text-right">Số tiền</th>
                                        <th class="py-3 px-4">Mục tiêu</th>
                                    </tr>
                                </thead>
                                <tbody class="divide-y divide-gray-100 bg-white">
                                    ${allocationHtml}
                                </tbody>
                            </table>
                        </div>
                        <div class="bg-white p-4 border-t border-gray-100 grid grid-cols-1 md:grid-cols-2 gap-4">
                            <div>
                                <p class="text-xs text-gray-500 uppercase tracking-wider mb-2 font-semibold">Trọng tâm của phương án</p>
                                <p class="text-sm text-gray-700 whitespace-pre-line leading-relaxed">${scenario.focus}</p>
                            </div>
                            <div>
                                <p class="text-xs text-gray-500 uppercase tracking-wider mb-2 font-semibold">Kết quả kỳ vọng</p>
                                <p class="text-sm text-gray-700 whitespace-pre-line leading-relaxed bg-brand-50 p-3 rounded-lg border border-brand-100">${scenario.expected_result}</p>
                            </div>
                        </div>
                    </div>
                `;
            }).join('');
        }

        const invDetailsContainer = document.getElementById('fsInvestmentDetails');
        if (invDetailsContainer && fs.investment_details) {
            invDetailsContainer.innerHTML = fs.investment_details.map(inv => `
                <div class="border border-gray-100 rounded-lg p-5 bg-white">
                    <h5 class="font-bold text-brand-700 text-sm mb-3">${inv.category}</h5>
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <div>
                            <p class="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2">Tại sao cần đầu tư?</p>
                            <p class="text-sm text-gray-700 leading-relaxed">${inv.why_invest}</p>
                        </div>
                        <div>
                            <p class="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2">Vấn đề cần giải quyết</p>
                            <ul class="space-y-1">
                                ${(inv.to_solve || []).map(item => `
                                    <li class="flex items-start gap-2 text-sm text-gray-700">
                                        <svg class="w-4 h-4 text-brand-500 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
                                        <span>${item}</span>
                                    </li>
                                `).join('')}
                            </ul>
                        </div>
                    </div>
                    <div class="mt-4 pt-4 border-t border-gray-50">
                        <p class="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-1">Kết quả kỳ vọng</p>
                        <p class="text-sm text-gray-700 font-medium">${inv.expected_result}</p>
                    </div>
                </div>
            `).join('');
        }

        document.getElementById('fsComparisonRationale').textContent = fs.comparison_rationale || '-';
        
        const compTableBody = document.getElementById('fsComparisonTable');
        if (compTableBody && fs.comparison_table) {
            compTableBody.innerHTML = fs.comparison_table.map(row => `
                <tr class="border-b border-gray-100 last:border-0 hover:bg-gray-50 transition-colors">
                    <td class="py-3 px-4 font-semibold text-gray-900">${row.category}</td>
                    <td class="py-3 px-4 text-gray-700">${row.scenario_a}</td>
                    <td class="py-3 px-4 text-brand-700 font-medium">${row.scenario_b}</td>
                </tr>
            `).join('');
        }

        document.getElementById('fsFinalAdvice').textContent = fs.final_advice || '-';

    } else {
        document.getElementById('fsContainer').classList.add('hidden');
    }

    // 5. Recommendations
    const recos = data.recommendations || [];
    const recoBody = document.getElementById('recoBody');
    recoBody.innerHTML = '';
    recos.forEach(r => {
        recoBody.innerHTML += `
            <tr class="border-b border-gray-100 last:border-0">
                <td class="py-4 px-4 font-medium text-gray-900">${r}</td>
            </tr>
        `;
    });

    // Show result section
    resultSec.classList.remove('hidden');
    resultSec.classList.add('fade-in-section');
    
    // Scroll to results smoothly
    setTimeout(() => {
        resultSec.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }, 100);
}

// Bind event listener
document.addEventListener('DOMContentLoaded', () => {
    const btn = document.getElementById('analyzeBtn');
    if (btn) {
        btn.addEventListener('click', handleAnalyze);
    }

    // File Upload Mockup Logic
    const uploadZone = document.getElementById('uploadZone');
    const fileInput = document.getElementById('fileInput');
    const uploadText = document.getElementById('uploadText');
    const uploadSubtext = document.getElementById('uploadSubtext');

    if (uploadZone && fileInput) {
        uploadZone.addEventListener('click', () => {
            fileInput.click();
        });

        // Drag and drop support
        uploadZone.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadZone.classList.add('bg-brand-50', 'border-brand-500');
        });

        uploadZone.addEventListener('dragleave', () => {
            uploadZone.classList.remove('bg-brand-50', 'border-brand-500');
        });

        uploadZone.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadZone.classList.remove('bg-brand-50', 'border-brand-500');
            if (e.dataTransfer.files.length > 0) {
                handleFileUpload(e.dataTransfer.files[0]);
            }
        });

        fileInput.addEventListener('change', (e) => {
            if (e.target.files.length > 0) {
                handleFileUpload(e.target.files[0]);
            }
        });
    }

    function handleFileUpload(file) {
        uploadText.innerHTML = `<span class="text-green-600 font-bold flex items-center justify-center gap-1"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg> Đã đính kèm tài liệu thành công!</span>`;
        uploadSubtext.textContent = `File: ${file.name} (${(file.size / 1024 / 1024).toFixed(2)} MB)`;
        
        // Optionally read text file to fill description (if txt/json)
        if (file.name.endsWith('.txt') || file.name.endsWith('.json')) {
            const reader = new FileReader();
            reader.onload = (e) => {
                const descInput = document.getElementById('descInput');
                if (descInput) {
                    descInput.value = e.target.result.substring(0, 500) + (e.target.result.length > 500 ? '...' : '');
                }
            };
            reader.readAsText(file);
        }
    }
});
