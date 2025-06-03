print("✔ main.py loaded")
from fastapi import FastAPI, File, UploadFile, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from PIL import Image
import io
import base64
import uvicorn
import os

app = FastAPI()

# Allow frontend JS fetch to work
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static and template files
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("landingpage.html", {"request": request})

def dehaze_image(image: Image.Image) -> Image.Image:
    return image  # Replace with ML logic

@app.post("/dehaze/")
async def dehaze(file: UploadFile = File(...)):
    image_bytes = await file.read()
    image = Image.open(io.BytesIO(image_bytes))
    output_image = dehaze_image(image)

    output_buffer = io.BytesIO()
    output_image.save(output_buffer, format="PNG")
    output_buffer.seek(0)
    encoded_image = base64.b64encode(output_buffer.read()).decode("utf-8")

    return JSONResponse(content={"dehazed_image": encoded_image})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=8000)
