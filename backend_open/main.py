from fastapi import FastAPI, UploadFile, File, Form, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import io
from PyPDF2 import PdfReader
from docx import Document as DocxDocument

# Import our modular components
from schemas import (
    DocumentAnalysisRequest, ScoreResponse, 
    FinancialCalculationRequest, MatcherRequest, FullAssessmentRequest
)
from matcher_engine import find_best_match, analyze_with_reference
from financial_calculator import calculate_financial_score
from ai_client import analyze_document_content, analyze_full_assessment

app = FastAPI(title="FundReady AI API - Open Source Version", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Helper function to extract text from file
def extract_text_from_file(file: UploadFile) -> str:
    content = file.file.read()
    filename = file.filename.lower()
    text = ""
    try:
        if filename.endswith(".pdf"):
            reader = PdfReader(io.BytesIO(content))
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        elif filename.endswith(".docx"):
            doc = DocxDocument(io.BytesIO(content))
            for para in doc.paragraphs:
                text += para.text + "\n"
        else:
            # Assume text or fallback
            text = content.decode("utf-8", errors="ignore")
    except Exception as e:
        print(f"Error extracting text from {filename}: {e}")
        text = f"[Lỗi trích xuất file {filename}]"
    return text.strip()

@app.get("/")
def root():
    return {"message": "FundReady AI API (Open Source) is running!"}

@app.post("/api/analyze-document", response_model=ScoreResponse)
def analyze_document(request: DocumentAnalysisRequest):
    result = analyze_document_content(request.document_type, request.content)
    return result

@app.post("/api/financial-calculate")
def calculate_financial(request: FinancialCalculationRequest):
    result = calculate_financial_score(request)
    return result

@app.post("/api/full-assessment")
def full_assessment(request: FullAssessmentRequest):
    # Combine all document contents
    combined_docs = "\n\n".join([f"--- {k} ---\n{v}" for k, v in request.documents.items()])
    result = analyze_full_assessment(combined_docs, request.financials)
    return result

@app.post("/api/match-profile")
def match_profile(request: MatcherRequest):
    matches = find_best_match(request.description, top_n=request.top_n)
    return {"matches": matches}

@app.post("/api/analyze-with-reference")
def analyze_with_reference_api(request: MatcherRequest):
    result = analyze_with_reference(request.description)
    return result

@app.post("/api/upload-document")
def upload_document(file: UploadFile = File(...), document_type: str = "pitchdeck"):
    text = extract_text_from_file(file)
    if not text:
        raise HTTPException(status_code=400, detail="Không thể trích xuất văn bản từ file.")
        
    return {
        "filename": file.filename,
        "document_type": document_type,
        "content": text[:50000] # Limit content length
    }

@app.post("/api/upload-multiple-documents")
def upload_multiple_documents(files: List[UploadFile] = File(...), document_type: str = "pitchdeck"):
    combined_text = ""
    file_details = []
    
    for file in files:
        text = extract_text_from_file(file)
        if text:
            combined_text += f"\n\n--- Document: {file.filename} ---\n{text}"
            file_details.append({"filename": file.filename, "status": "success"})
        else:
            file_details.append({"filename": file.filename, "status": "failed"})
            
    if not combined_text:
        raise HTTPException(status_code=400, detail="Không có file nào được trích xuất thành công.")
        
    return {
        "document_type": document_type,
        "files_processed": file_details,
        "content": combined_text[:100000]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)
