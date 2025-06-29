from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from PIL import Image
import pytesseract
import os

app = FastAPI()

# 템플릿, 정적 폴더 설정
templates = Jinja2Templates(directory="templates")
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# 업로드 폴더
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.get("/", response_class=HTMLResponse)
async def form(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})

@app.post("/upload/")
async def upload_file(request: Request, file: UploadFile = File(...)):
    contents = await file.read()
    filename = os.path.join(UPLOAD_FOLDER, file.filename)

    # 파일 저장
    with open(filename, "wb") as f:
        f.write(contents)

    # 이미지 열기 및 OCR
    image = Image.open(filename)
    extracted_text = pytesseract.image_to_string(image, lang='kor+eng')

    return templates.TemplateResponse("upload.html", {
        "request": request,
        "extracted_text": extracted_text,
        "uploaded": True,
        "filename": file.filename
    })