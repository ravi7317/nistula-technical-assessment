import sys
import uvicorn
from fastapi import FastAPI
from app.routes import webhook
from app.config import Config

# Fix for Emoji Corruption on Windows Terminal
# Ensures that emojis in Claude's 'WhatsApp-native' responses are handled correctly.
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

app = FastAPI(
    title="Nistula Guest Message Handler",
    description="Backend service for handling and classifying multi-channel guest messages."
)

# Registering our API routes
app.include_router(webhook.router)

if __name__ == "__main__":
    print(f"Starting Nistula Message Handler on port {Config.PORT}...")
    uvicorn.run(app, host="0.0.0.0", port=Config.PORT)
