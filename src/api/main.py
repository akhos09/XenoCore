from fastapi import FastAPI

app = FastAPI(title="XenoCoreAPI", docs_url="/docs")

@app.get("/")
async def test():
    return "Hello World"
