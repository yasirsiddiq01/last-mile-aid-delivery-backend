from fastapi import FastAPI

app = FastAPI(
    title="Last-Mile Aid Delivery Monitoring Backend",
    description="Portfolio backend API for monitoring humanitarian last-mile aid deliveries.",
    version="0.1.0",
)


@app.get("/")
def root():
    return {
        "message": "Last-Mile Aid Delivery Monitoring Backend is running",
        "docs_url": "/docs",
        "health_url": "/health",
    }


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "last-mile-aid-delivery-backend",
        "version": "0.1.0",
    }