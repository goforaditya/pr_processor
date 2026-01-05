import os
import shutil
from typing import List
from fastapi import FastAPI, File, UploadFile, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.extractor import PRExtractor
from app.educator import PREducator

app = FastAPI(title="Purchase Request Processor")

# Directories
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Templates
templates = Jinja2Templates(directory="./app/templates")

# Mount samples
app.mount("/samples", StaticFiles(directory="sample_prs"), name="samples")

# Services
extractor = PRExtractor()

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("compare.html", {"request": request, "result": None})

@app.post("/compare", response_class=HTMLResponse)
async def compare_prs(
    request: Request,
    file1: UploadFile = File(...),
    file2: UploadFile = File(...)
):
    # Save files
    files = [file1, file2]
    saved_paths = []
    
    for file in files:
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        saved_paths.append(file_path)

    # Extract Data
    data1 = await extractor.extract_data(saved_paths[0])
    data2 = await extractor.extract_data(saved_paths[1])

    # Check for errors
    errors = []
    if "error" in data1: errors.append(f"File 1 Error: {data1['error']}")
    if "error" in data2: errors.append(f"File 2 Error: {data2['error']}")
    
    if errors:
         return templates.TemplateResponse("compare.html", {
             "request": request, 
             "error": " | ".join(errors)
         })

    # Compare
    comparison = PREducator.compare_prs(data1, data2)
    
    return templates.TemplateResponse("compare.html", {
        "request": request, 
        "result": comparison,
        "data1": data1,
        "data2": data2
    })
