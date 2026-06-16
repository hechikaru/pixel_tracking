import time
from fastapi import FastAPI, Response, Request

app = FastAPI()

TRANSPARENT_1X1_PNG = (
    b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01"
    b"\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\rIDATx\x9cc`0\x00"
    b"\x00\x00\x02\x00\x01H\xaf\xa4q\x00\x00\x00\x00IEND\xaeB`\x82"
)

@app.middleware("http")
async def log_incoming_traffic(request: Request, call_next):
    # This will print directly to your Render dashboard web log screen
    print(f"\n[CLOUD INBOUND] Path: {request.url.path} | Method: {request.method}")
    print(f"[USER-AGENT] {request.headers.get('user-agent')}")
    return await call_next(request)

@app.get("/track/{user_id}/pixel.png")
async def track_open(user_id: str, response: Response):
    # Calculate the exact size of your binary image
    content_length = str(len(TRANSPARENT_1X1_PNG))

    # Force strict image headers so Google doesn't think it's corrupted text
    response.headers["Content-Length"] = content_length
    response.headers["Content-Type"] = "image/png"

    # Forcing Google Proxy to fetch fresh on every single load loop
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return Response(content=TRANSPARENT_1X1_PNG, media_type="image/png")

# @app.get("/track/{user_id}/banner.png")
# async def track_and_redirect(user_id: str):
#     # This logs the live user hit
#     print(f"\n[REAL OPEN EVENT] User {user_id} requested the image payload!")
    
#     # Redirect to a high-quality static image hosted on a completely different CDN
#     # Google will execute your code first, then grab the asset
#     target_image = "https://unsplash.com"
    
#     response = RedirectResponse(url=target_image, status_code=302)
#     response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, max-age=0"
#     return response
