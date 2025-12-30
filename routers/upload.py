
from fastapi import APIRouter, UploadFile, File, HTTPException
from uuid import uuid4
import os
import shutil


router = APIRouter()


UPLOAD_IDR = "static/uploads"

os.makedirs(UPLOAD_IDR,exist_ok=True)

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="只允许上传图片")

    # 生成唯一文件名
    file_ext = os.path.splitext(file.filename)[1]
    new_filename = f"{uuid4()}{file_ext}"

    #拼接完整保存路径
    file_path = os.path.join(UPLOAD_IDR, new_filename)

    #写入文件
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file,buffer)
    except Exception as e:
        raise HTTPException(status_code=500,detail="文件保存失败")

    url = f"/static/uploads/{new_filename}"

    return {"url": url, "filename": new_filename}
