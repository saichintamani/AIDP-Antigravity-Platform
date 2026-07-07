from fastapi import FastAPI

from aidp.platform.api.routes import router

app = FastAPI(
    title="AIDP (Artificial Intelligence Discovery Platform)",
    description="API Gateway for the Autonomous Scientific Laboratory.",
    version="0.1.0",
)

app.include_router(router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
