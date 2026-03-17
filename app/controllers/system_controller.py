from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health():
    return {"status": "ok"}


@router.get("/.well-known/appspecific/com.chrome.devtools.json")
async def chrome_devtools():
    return {}
