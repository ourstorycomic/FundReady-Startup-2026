// Tự động nhận diện môi trường: Nếu chạy trên máy tính (localhost) thì gọi cổng 8001, nếu trên Vercel thì gọi chính domain của Vercel.
const API_BASE = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' 
    ? "http://localhost:8001" 
    : "";

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
        const docType = document.getElementById('docType') ? document.getElementById('docType').value : 'pitchdeck';
        const fundingInput = document.getElementById('fundingAmount');
        const desired_amount = fundingInput ? fundingInput.value.trim() : '';

        const response = await fetch(`${API_BASE}/api/analyze-document`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ document_type: docType, content: desc, desired_amount: desired_amount })
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
        const maxScore = b.maximum || b.max || 10;
        const pct = (b.score / maxScore) * 100;
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
                        <span class="text-sm font-bold text-gray-700 w-12">${b.score}/${maxScore}</span>
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
        renderSimulation(data.funding_scenario);
    } else {
        const simResult = document.getElementById('simResult');
        if (simResult) simResult.classList.add('hidden');
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
                    descInput.value = e.target.result;
                }
            };
            reader.readAsText(file);
        }
    }
});


function renderSimulation(data) {
    const simResult = document.getElementById('simResult');
    if (simResult) simResult.classList.remove('hidden');
    
    // Helper function to render allocations
    const renderAllocations = (allocations) => {
        if (!allocations || !allocations.length) return '';
        return allocations.map(al => `
            <div class="mb-5 border border-gray-100 rounded-lg p-4 bg-white shadow-sm hover:shadow-md transition-all">
                <div class="flex justify-between items-center border-b border-gray-100 pb-2 mb-3">
                    <p class="font-bold text-gray-800 text-base">${al.category}</p>
                    <div class="text-right">
                        <span class="text-brand-600 font-bold text-lg">${al.amount}</span> 
                        <span class="text-xs text-gray-500 bg-gray-100 px-2 py-1 rounded-full ml-1">${al.percentage || ''}</span>
                    </div>
                </div>
                <div class="mb-3">
                    <p class="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-1">Mục tiêu & Lý do đầu tư</p>
                    <p class="text-sm text-gray-700 leading-relaxed">${al.why_invest || al.objective || ''}</p>
                </div>
                ${al.action_items && al.action_items.length > 0 ? `
                <div class="bg-gray-50 p-3 rounded-md border border-gray-100">
                    <p class="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2">Các vấn đề cần giải quyết</p>
                    <ul class="list-disc pl-5 space-y-1">
                        ${al.action_items.map(item => `<li class="text-sm text-gray-700">${item}</li>`).join('')}
                    </ul>
                </div>
                ` : ''}
            </div>
        `).join('');
    };

    const scenarios = data.scenarios || [];
    let scenariosHTML = '';
    
    if (scenarios.length === 0) {
        scenariosHTML = '<p class="text-sm text-gray-500 italic p-6">Không có dữ liệu kịch bản phân bổ.</p>';
    } else {
        scenariosHTML = scenarios.map((scenario, index) => {
            const isRecommended = index === 0; // Giả sử phương án đầu là khuyến nghị
            const allocationsHTML = renderAllocations(scenario.allocation);
            return `
            <div class="flex flex-col border-2 ${isRecommended ? 'border-brand-400' : 'border-gray-200'} bg-white rounded-xl shadow-md hover:shadow-xl transition-shadow relative">
                ${isRecommended ? '<div class="absolute -top-3 right-5 bg-brand-600 text-white text-xs font-black px-4 py-1.5 rounded-full shadow-md uppercase tracking-widest border-2 border-white">Khuyến nghị</div>' : ''}
                <div class="${isRecommended ? 'bg-brand-50 border-brand-100' : 'bg-gray-50 border-gray-200'} px-6 py-4 border-b rounded-t-xl">
                    <h3 class="font-black text-xl ${isRecommended ? 'text-brand-900' : 'text-gray-900'}">${scenario.name || `Phương án ${String.fromCharCode(65 + index)}`}</h3>
                </div>
                <div class="p-6 flex-grow">
                    <div class="mb-6 ${isRecommended ? 'bg-brand-50 border-brand-100 text-brand-900' : 'bg-yellow-50 border-yellow-100 text-yellow-900'} p-4 rounded-lg border">
                        <p class="text-xs font-bold uppercase tracking-wider mb-2 ${isRecommended ? 'text-brand-800' : 'text-yellow-800'}">Trọng tâm chiến lược</p>
                        <p class="text-sm leading-relaxed">${scenario.focus_explanation || scenario.focus || ''}</p>
                    </div>
                    <div class="mb-6">
                        <h4 class="font-bold text-gray-800 mb-4 border-b pb-2">Chi tiết phân bổ</h4>
                        ${allocationsHTML}
                    </div>
                    ${scenario.expected_results && scenario.expected_results.length > 0 ? `
                    <div class="bg-indigo-50/50 p-5 rounded-lg border border-indigo-100 mt-auto">
                        <h4 class="font-bold text-indigo-900 mb-3 text-sm uppercase tracking-wider">Kết quả kỳ vọng</h4>
                        <ul class="space-y-2">
                            ${scenario.expected_results.map(r => `
                                <li class="flex items-start">
                                    <svg class="w-5 h-5 text-indigo-500 mr-2 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
                                    <span class="text-sm text-gray-700 leading-relaxed">${r}</span>
                                </li>
                            `).join('')}
                        </ul>
                    </div>
                    ` : ''}
                </div>
            </div>
            `;
        }).join('');
    }

    let dealHTML = '';
    if (data.suggested_deal) {
        dealHTML = `
            <div class="bg-gradient-to-r from-brand-50 to-white border border-brand-100 rounded-xl p-6 mb-8 shadow-sm">
                <h3 class="font-bold text-brand-900 mb-4 text-lg flex items-center">
                    <svg class="w-5 h-5 mr-2 text-brand-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg>
                    Đề xuất Cấu trúc Deal & Định giá
                </h3>
                <div class="grid grid-cols-2 md:grid-cols-4 gap-6">
                    <div class="bg-white p-4 rounded-lg border border-brand-50 shadow-sm text-center">
                        <p class="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-1">Công cụ</p>
                        <p class="font-bold text-brand-800 text-lg">${data.suggested_deal.instrument}</p>
                    </div>
                    <div class="bg-white p-4 rounded-lg border border-brand-50 shadow-sm text-center">
                        <p class="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-1">Pre-money</p>
                        <p class="font-bold text-brand-800 text-lg">${data.suggested_deal.pre_money}</p>
                    </div>
                    <div class="bg-white p-4 rounded-lg border border-brand-50 shadow-sm text-center">
                        <p class="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-1">Post-money</p>
                        <p class="font-bold text-brand-800 text-lg">${data.suggested_deal.post_money}</p>
                    </div>
                    <div class="bg-white p-4 rounded-lg border border-brand-50 shadow-sm text-center">
                        <p class="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-1">Pha loãng</p>
                        <p class="font-bold text-brand-800 text-lg">${data.suggested_deal.dilution}</p>
                    </div>
                </div>
                ${data.suggested_deal.note ? `<p class="mt-4 text-sm text-gray-600 italic text-center">* ${data.suggested_deal.note}</p>` : ''}
            </div>
        `;
    }

    const rationale = data.rationale || {};

    simResult.innerHTML = `
        <div class="w-full mt-10 mb-8">
            <h2 class="font-black text-2xl text-gray-900 mb-6 pb-3 border-b-2 border-brand-500 uppercase tracking-tight flex items-center">
                <svg class="w-7 h-7 mr-3 text-brand-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path></svg>
                Phân tích & Mô phỏng Kịch bản Gọi vốn
            </h2>
            
            <div class="bg-white rounded-xl border border-gray-200 shadow-md overflow-hidden mb-8">
                <div class="bg-gray-50 px-6 py-4 border-b border-gray-200">
                    <h3 class="font-bold text-gray-900 text-lg">1. Nhận định & Đề xuất mức vốn</h3>
                </div>
                <div class="p-6">
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                        <div class="bg-red-50 rounded-lg p-5 border border-red-100 flex flex-col justify-center items-center text-center">
                            <p class="text-sm font-semibold text-red-800 uppercase tracking-wider mb-2">Mức vốn doanh nghiệp mong muốn</p>
                            <p class="text-3xl font-black text-red-600">${data.desired_amount || '-'}</p>
                        </div>
                        <div class="bg-green-50 rounded-lg p-5 border border-green-100 flex flex-col justify-center items-center text-center relative overflow-hidden">
                            <div class="absolute top-0 right-0 bg-green-500 text-white text-[10px] font-bold px-2 py-1 rounded-bl-lg uppercase tracking-wider">Hệ thống Đề xuất</div>
                            <p class="text-sm font-semibold text-green-800 uppercase tracking-wider mb-2">Mức vốn hệ thống khuyến nghị</p>
                            <p class="text-3xl font-black text-green-600">${data.recommended_amount || '-'}</p>
                        </div>
                    </div>
                    
                    <div class="bg-blue-50/50 rounded-lg p-5 border border-blue-100">
                        <p class="text-sm font-bold text-blue-900 uppercase tracking-wider mb-3">Tại sao hệ thống đề xuất mức này?</p>
                        <p class="text-base text-gray-800 leading-relaxed mb-5">${rationale.why_recommended || '-'}</p>
                        
                        <p class="text-sm font-bold text-blue-900 uppercase tracking-wider mb-3">Nhu cầu đầu tư cốt lõi:</p>
                        <div class="grid grid-cols-1 md:grid-cols-3 gap-3">
                            ${(rationale.investment_needs || []).map((need, idx) => `
                                <div class="bg-white rounded border border-blue-100 p-3 flex items-start shadow-sm">
                                    <div class="bg-blue-100 text-blue-800 rounded-full w-6 h-6 flex items-center justify-center font-bold text-xs mr-3 flex-shrink-0">${idx + 1}</div>
                                    <p class="text-sm text-gray-700 leading-tight">${need}</p>
                                </div>
                            `).join('')}
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <h3 class="font-bold text-gray-900 text-xl mb-5">2. Các phương án phân bổ vốn chi tiết</h3>
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-10">
            ${scenariosHTML}
        </div>

        ${dealHTML}

        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
            <div class="bg-gray-900 text-white rounded-xl p-6 shadow-lg">
                <h3 class="font-bold text-gray-100 mb-4 text-lg border-b border-gray-700 pb-2 flex items-center">
                    <svg class="w-5 h-5 mr-2 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 18.657A8 8 0 016.343 7.343S7 9 9 10c0-2 .5-5 2.986-7C14 5 16.09 5.777 17.656 7.343A7.975 7.975 0 0120 13a7.975 7.975 0 01-2.343 5.657z"></path><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.879 16.121A3 3 0 1012.015 11L11 14H9c0 .768.293 1.536.879 2.121z"></path></svg>
                    Đánh giá Burn Rate & Runway
                </h3>
                <p class="text-sm text-gray-300 leading-relaxed">${data.burn_rate_runway || 'Chưa xác định'}</p>
            </div>
            
            <div class="bg-white border border-gray-200 rounded-xl p-6 shadow-sm">
                <h3 class="font-bold text-gray-900 mb-4 text-lg border-b pb-2 flex items-center">
                    <svg class="w-5 h-5 mr-2 text-indigo-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                    Lộ trình Giải ngân & Mục tiêu
                </h3>
                <div class="space-y-4">
                    ${data.milestones ? data.milestones.map(m => `
                        <div class="flex items-start">
                            <div class="flex flex-col items-center mr-4">
                                <div class="w-3 h-3 bg-indigo-500 rounded-full mt-1.5"></div>
                                <div class="w-0.5 h-full bg-indigo-100 my-1"></div>
                            </div>
                            <div class="pb-2">
                                <p class="text-sm font-bold text-indigo-900 uppercase tracking-wider mb-1">${m.phase}</p>
                                <p class="text-sm text-gray-600 leading-relaxed">${m.goal}</p>
                            </div>
                        </div>
                    `).join('') : '<p class="text-sm text-gray-500">Không có dữ liệu lộ trình giải ngân.</p>'}
                </div>
            </div>
        </div>

        <div class="bg-gradient-to-r from-gray-50 to-gray-100 border-l-4 border-brand-500 p-6 rounded-r-xl shadow-sm">
            <h3 class="font-bold text-gray-900 mb-2 text-lg">Khuyến nghị cuối cùng từ AI</h3>
            <p class="text-base text-gray-800 leading-relaxed font-medium">${data.final_recommendation || data.conclusion || 'Startup cần xem xét kỹ các phương án trên.'}</p>
        </div>
    `;
    
    // Scroll to results smoothly
    setTimeout(() => {
        simResult.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }, 200);
}
