from fastapi import FastAPI, Response, Request

app = FastAPI()

# A globally verified, industry-standard 1x1 transparent GIF byte array (43 bytes)
# Much more reliable through proxy architectures than custom PNG streams
TRANSPARENT_1X1_GIF = (
    b"\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00"
    b"\xff\xff\xff\x21\xf9\x04\x01\x00\x00\x00\x00\x2c\x00\x00\x00\x00"
    b"\x01\x00\x01\x00\x00\x02\x02\x4c\x01\x00\x3b"
)

@app.middleware("http")
async def log_incoming_traffic(request: Request, call_next):
    print(f"\n[CLOUD INBOUND] Path: {request.url.path} | Method: {request.method}")
    print(f"[USER-AGENT] {request.headers.get('user-agent')}")
    return await call_next(request)

@app.get("/track/{user_id}/pixel.gif")  # Changed extension to .gif for purity
async def track_open(user_id: str):
    print(f"[SUCCESS] Email opened by user ID: {user_id}")
    
    # Constructing a direct Response container maps headers flawlessly through middleware
    return Response(
        content=TRANSPARENT_1X1_GIF,
        media_type="image/gif",
        headers={
            "Content-Length": str(len(TRANSPARENT_1X1_GIF)),
            "Cache-Control": "no-cache, no-store, must-revalidate, max-age=0",
            "Pragma": "no-cache",
            "Expires": "0"
        }
    )
