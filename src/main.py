from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import uvicorn
from typing import Optional
import uuid
from datetime import datetime
from src.bonk_mcp import settings
from src.bonk_mcp.tools import token_launcher_tool, token_buyer_tool

# Initialize FastAPI app
app = FastAPI(
    title="Bonk Token Launcher",
    description="API for launching Bonk tokens",
    version="0.1.0"
)

# Model for token launch request


class TokenLaunchRequest(BaseModel):
    name: str
    symbol: str
    description: Optional[str] = None
    twitter: Optional[str] = None
    telegram: Optional[str] = None
    website: Optional[str] = None
    image_url: str = Field(default=settings.DEFAULT_IMAGE_URL)


class TokenBuyerRequest(BaseModel):
    token_address: str
    amount_sol: float
    slippage: Optional[float] = 5.0  # Default to 5% slippage
    keypair: str  # Should be a base58 encoded string of the private key

# Model for token launch response


class TokenLaunchResponse(BaseModel):
    token_id: str
    name: str
    description: Optional[str] = None
    amount: float
    recipient_address: str
    timestamp: datetime
    status: str


@app.post("/launch-token")
async def launch_token(arguments: TokenLaunchRequest):
    """
    Launch a new Bonk token to the specified address

    This endpoint processes token launch requests and returns the status.
    """
    try:
        if settings.ENVIRONMENT == "dev":
            return {
                "mint_address": "7Z7zLN3TWN49YYWLCkH4neCoJ4UAGvxsFZz2Ho3D9kQ",
                "pool_state": "B9M9mAixNDP7hJkxVGZNQXhYEae6K9PBxGnavR3zhHXi",
                "uri": "https://sapphire-working-koi-276.mypinata.cloud/ipfs/bafkreibhmzxivrpgy53jiyb4pjk2x4chm5arimzppyky6zgluiltclwhiy/nImage",
                "image_url": "https://img.cryptorank.io/coins/bonk1672306100278.png"
            }
        # In a real implementation, this would interact with the Solana blockchain
        # using the solana and solders packages from requirements.txt

        # Generate a unique ID for this token launch

        # Return the response with launch details
        return await token_launcher_tool.execute(arguments.model_dump())
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Token launch failed: {str(e)}")


class CustomException(Exception):
    def __init__(self, content: object):
        self.content = content


@app.exception_handler(CustomException)
async def unicorn_exception_handler(request: Request, exc: CustomException):
    return JSONResponse(
        status_code=400,
        content=exc.content
    )


@app.post("/buy-token")
async def buy_token(arguments: TokenBuyerRequest):
    """
    Buy a Bonk token from the specified address

    This endpoint processes token purchase requests and returns the status.
    """
    # In a real implementation, this would interact with the Solana blockchain
    # using the solana and solders packages from requirements.txt

    # Generate a unique ID for this token purchase

    # Return the response with purchase details
    if arguments.token_address == "7Z7zLN3TWN49YYWLCkH4neCoJ4UAGvxsFZz2Ho3D9kQ":
        return {
            "code": 200,
            "message": {
                "mint_address": "7Z7zLN3TWN49YYWLCkH4neCoJ4UAGvxsFZz2Ho3D9kQ",
                "sol_spent": 0.01,
                "tokens_received": 338608.5429429687,
                "transaction_hash": "46WCtfzDeL3JVHu82JrW6sQCBEaWSexVXLW2FqovXTMnMfWdTQgyYMYexPw885kei1aed4SksjTvuKUge3XX9Mwb"
            }
        }
    else:
        raise CustomException(content={
            "code": 500,
            "message": "Buy token failed: Invalid token address"
        })

    response = await token_buyer_tool.execute(arguments.model_dump())
    if response["code"] == 200:
        return response
    else:
        raise CustomException(content=response)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
