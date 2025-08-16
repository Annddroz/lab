from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, AnyHttpUrl
from .storage import get_client, key_for
from starlette.responses import RedirectResponse

app = FastAPI(title="URL Shortener", version="1.0.0")

class UrlIn(BaseModel):
    url: AnyHttpUrl

@app.on_event("startup")
def startup():
    # בדיקה מוקדמת ש-Redis זמין (לא תעצור את השירות אם לא)
    try:
        r = get_client()
        r.ping()
    except Exception:
        pass

@app.post("/shorten")
def shorten(item: UrlIn):
    r = get_client()
    code = key_for(item.url)
    r.set(code, str(item.url))
    return {"code": code, "short": f"/{code}"}

@app.get("/{code}")
def resolve(code: str):
    r = get_client()
    target = r.get(code)
    if not target:
        raise HTTPException(status_code=404, detail="Code not found")
    return RedirectResponse(url=target.decode("utf-8"), status_code=307)

