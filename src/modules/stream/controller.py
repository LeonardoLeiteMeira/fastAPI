from fastapi import APIRouter
from fastapi.responses import StreamingResponse

router = APIRouter(tags=["Stream"])

async def fake_video_streamer():
    for i in range(10000000):
        # yield b"test"
        yield "{} some fake video bytes\n".format(i)

@router.get("/")
async def simple_get():
    return StreamingResponse(fake_video_streamer())