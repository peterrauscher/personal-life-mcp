import os
import httpx
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

CREATE_REMINDER_WEBHOOK_URL = os.environ.get("CREATE_REMINDER_WEBHOOK_URL")
BEARER_TOKEN = os.environ.get("BEARER_TOKEN")

app = FastAPI(
    title="Peter's Life Assistant API",
    version="0.1.0",
)

bearer_scheme = HTTPBearer()


def validate_token(credentials: str = Depends(bearer_scheme)):
    if not BEARER_TOKEN:
        raise HTTPException(
            status_code=500, detail="Authentication token not configured on server"
        )
    if credentials.credentials != BEARER_TOKEN:
        raise HTTPException(
            status_code=401,
            detail="Invalid bearer token",
            headers={"WWW-Authenticate": "Bearer"},
        )


class Reminder(BaseModel):
    title: str
    startDate: str
    dueDate: str
    alarm: str
    note: str


@app.post("/create_reminder", status_code=201, dependencies=[Depends(validate_token)])
async def create_reminder(reminder: Reminder):
    """
    Receives reminder data, validates it, and forwards it to a webhook.
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                CREATE_REMINDER_WEBHOOK_URL,
                json=reminder.dict(),
                headers={"Content-Type": "application/json"},
            )
            response.raise_for_status()

            try:
                response_data = response.json()
            except Exception:
                response_data = response.text

            return {"status": "success", "response": response_data}

    except httpx.HTTPStatusError as exc:
        raise HTTPException(
            status_code=exc.response.status_code,
            detail=f"Error from webhook: {exc.response.text}",
        )
    except httpx.RequestError as exc:
        raise HTTPException(
            status_code=500, detail=f"Could not connect to webhook: {exc}"
        )
