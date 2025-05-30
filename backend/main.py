import os
from datetime import datetime
from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
from typing import List
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Image Moderation API")

# --- CORS Middleware Setup ---
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    # Add other origins if needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Or ["*"] to allow all for dev only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB Setup
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
client = AsyncIOMotorClient(MONGODB_URI)
db = client.image_moderation
tokens_collection = db.tokens
usage_collection = db.usages

# Security
security = HTTPBearer()

# Pydantic models
class TokenModel(BaseModel):
    token: str
    isAdmin: bool = False
    createdAt: datetime

class TokenCreateRequest(BaseModel):
    isAdmin: bool = False

class TokenResponse(BaseModel):
    token: str
    isAdmin: bool
    createdAt: datetime

class SafetyCategory(BaseModel):
    category: str
    confidence: float

class SafetyReport(BaseModel):
    categories: List[SafetyCategory]

# Helper functions
async def verify_token(auth: HTTPAuthorizationCredentials = Depends(security)):
    token = auth.credentials
    token_doc = await tokens_collection.find_one({"token": token})
    if not token_doc:
        raise HTTPException(status_code=401, detail="Invalid token")
    return token_doc

async def verify_admin_token(token_doc=Depends(verify_token)):
    if not token_doc.get("isAdmin", False):
        raise HTTPException(status_code=403, detail="Admin privileges required")
    return token_doc

async def log_usage(token: str, endpoint: str):
    await usage_collection.insert_one({
        "token": token,
        "endpoint": endpoint,
        "timestamp": datetime.utcnow()
    })

# Authentication Endpoints (Admin only)
@app.post("/auth/tokens", response_model=TokenResponse)
async def create_token(req: TokenCreateRequest, admin=Depends(verify_admin_token)):
    import secrets
    new_token = secrets.token_urlsafe(32)
    token_doc = {
        "token": new_token,
        "isAdmin": req.isAdmin,
        "createdAt": datetime.utcnow()
    }
    await tokens_collection.insert_one(token_doc)
    return token_doc

@app.get("/auth/tokens", response_model=List[TokenResponse])
async def list_tokens(admin=Depends(verify_admin_token)):
    tokens_cursor = tokens_collection.find()
    tokens = []
    async for token_doc in tokens_cursor:
        tokens.append(TokenResponse(**token_doc))
    return tokens

@app.delete("/auth/tokens/{token}")
async def delete_token(token: str, admin=Depends(verify_admin_token)):
    result = await tokens_collection.delete_one({"token": token})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Token not found")
    return {"detail": "Token deleted"}

# Moderation Endpoint
@app.post("/moderate", response_model=SafetyReport)
async def moderate_image(file: UploadFile = File(...), token_doc=Depends(verify_token)):
    await log_usage(token_doc["token"], "/moderate")

    import random

    categories_possible = [
        "Graphic Violence",
        "Hate Symbols",
        "Explicit Nudity",
        "Self-Harm Depictions",
        "Extremist Propaganda",
        "Safe"
    ]

    content = await file.read()
    size_kb = len(content) / 1024
    if size_kb > 1024:
        categories = [
            {"category": "Graphic Violence", "confidence": 0.75},
            {"category": "Hate Symbols", "confidence": 0.25}
        ]
    else:
        categories = [{"category": "Safe", "confidence": 0.99}]

    return {"categories": categories}
