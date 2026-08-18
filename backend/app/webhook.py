import hmac, hashlib, json
from fastapi import APIRouter, Request, HTTPException, Header, BackgroundTasks
from app.config import settings
from app.background import process_review
 
router = APIRouter()
 
def verify_signature(payload_body: bytes, signature_header: str) -> bool:
    if not signature_header:
        return False
    hash_object = hmac.new(
        settings.GITHUB_WEBHOOK_SECRET.encode(), msg=payload_body, digestmod=hashlib.sha256
    )
    expected_signature = "sha256=" + hash_object.hexdigest()
    return hmac.compare_digest(expected_signature, signature_header)
 
@router.post("/webhook/github")
async def github_webhook(
    request: Request,
    background_tasks: BackgroundTasks,
    x_hub_signature_256: str = Header(None),
    x_github_event: str = Header(None),
):
    body = await request.body()
    if not verify_signature(body, x_hub_signature_256):
        raise HTTPException(status_code=401, detail="Invalid signature")
 
    payload = json.loads(body)
 
    if x_github_event == "pull_request" and payload.get("action") in (
        "opened", "synchronize", "reopened",
    ):
        repo_name = payload["repository"]["full_name"]
        pr_number = payload["pull_request"]["number"]
        # Queue the job — DO NOT process synchronously here.
        background_tasks.add_task(process_review, repo_name, pr_number)
        return {"status": "queued"}
 
    return {"status": "ignored"}