from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import StreamingResponse
from stencil import generate_stencil

app = FastAPI()

@app.post("/stencil")
async def create_stencil(
    image: UploadFile = File(...),
    line_thickness: int = Form(2)
):
    image_bytes = await image.read()
    result = generate_stencil(image_bytes, line_thickness)
    return StreamingResponse(result, media_type="image/png")
