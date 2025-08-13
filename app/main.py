from fastapi import FastAPI
from app.api.router import router as api_router
from app.db.session import engine
import asyncio


app = FastAPI()


app.include_router(api_router, prefix="/v1/api")

@app.on_event("startup")
async def on_startup():
    try:
        #test DB connection
        async with engine.connect() as conn:
            await conn.run_sync(lambda conn: None)
        print("✅ Database connection successful.")

    except Exception as e:
        print(f"❌ Database connection failed: {e}")

@app.get("/")
async def root():
    return { "message": "BE ExplainIt.Tech up and Running" }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)