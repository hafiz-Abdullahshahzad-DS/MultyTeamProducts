from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from starlette.responses import HTMLResponse
import os

app = FastAPI()

# Define paths for uploaded files
UPLOAD_DIR = "uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

@app.get("/", response_class=HTMLResponse)
async def main_page():
    with open("templates/index.html") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)

@app.post("/upload1")
async def upload_file1(file1: UploadFile = File(...)):
    file_location = f"{UPLOAD_DIR}/file1_{file1.filename}"
    with open(file_location, "wb") as file_out:
        file_out.write(await file.read())
    return {"info": "Document 1 uploaded successfully"}

@app.post("/upload2")
async def upload_file2(file2: UploadFile = File(...)):
    file_location = f"{UPLOAD_DIR}/file2_{file2.filename}"
    with open(file_location, "wb") as file_out:
        file_out.write(await file.read())
    return {"info": "Document 2 uploaded successfully"}

@app.get("/download")
async def download_file():
    # Path to your text file
    text_file_path = "path/to/your/textfile.txt"
    return FileResponse(text_file_path, filename="downloaded_file.txt")
