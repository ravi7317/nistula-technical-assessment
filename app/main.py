from fastapi import FastAPI
from app.routes import webhook
from app.config import Config

app = FastAPI(
    title="Nistula Guest Message Handler",
    description="Backend service for handling and classifying multi-channel guest messages."
)

# Registering our API routes
app.include_router(webhook.router)

if __name__ == "__main__":
    import uvicorn
    print(f"Starting Nistula Message Handler on port {Config.PORT}...")
    uvicorn.run(app, host="0.0.0.0", port=Config.PORT)
