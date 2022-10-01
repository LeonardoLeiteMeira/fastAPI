from fastapi import FastAPI
import uvicorn
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World leoooo"}


if __name__ == "__main__":
    uvicorn.Config(reload=True, debug=True)
    uvicorn.run(app,host="0.0.0.0",port=8000)
