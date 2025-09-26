import shutil
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from PIL import Image
import io
import os

from app.core.config import settings
from app.core.utils import generate_unique_id




# >>>>>>> Handle Image Uplaod <<<<<<<<<
UPLOAD_DIR = "uploads/"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def compress_and_resize_image(
    image_bytes: bytes, max_size: int = 800, quality: int = 70
) -> bytes:
    """
    Compress and resize an image using Pillow.
    
    :param image_bytes: Original image in bytes
    :param max_size: Maximum width/height in pixels
    :param quality: Compression quality (1-100)
    :return: Processed image bytes
    """
    try:
        image = Image.open(io.BytesIO(image_bytes))
        img_format = image.format  # Preserve original format

        # Convert if necessary (JPEG doesn’t support transparency)
        if img_format == "JPEG" and image.mode in ("RGBA", "P"):
            image = image.convert("RGB")

        # Resize while maintaining aspect ratio
        if max(image.size) > max_size:
            image.thumbnail((max_size, max_size))

        compressed_io = io.BytesIO()
        image.save(compressed_io, format=img_format, optimize=True, quality=quality)
        return compressed_io.getvalue()

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Image processing failed: {e}")
    


async def upload_image(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File is not an image")
    

    # Generate a unique filename for the uploaded image
    file_extension = file.filename.split(".")[-1]
    filename = f"{generate_unique_id(15)}.{file_extension}"

    try:
        contents = await file.read()

        # Compress + resize
        processed_bytes = compress_and_resize_image(contents, max_size=800, quality=70)

        # Save processed image
        save_path = os.path.join(UPLOAD_DIR+filename)
        with open(save_path, "wb") as f:
            f.write(processed_bytes)



        return f"{settings.baseurl}/{save_path}"

        # return JSONResponse(
        #     content={
        #         "filename": file.filename,
        #         "original_size_kb": round(len(contents) / 1024, 2),
        #         "processed_size_kb": round(len(processed_bytes) / 1024, 2),
        #         "saved_path": save_path,
        #     }
        # )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload image: {e}")