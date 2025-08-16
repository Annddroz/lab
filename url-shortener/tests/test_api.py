import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client():
    return TestClient(app)

def test_shorten_and_redirect(monkeypatch, client):
    # מחליפים Redis ב-fake קל כדי שהבדיקות רצות בלי Redis אמיתי
    class FakeRedis:
        def __init__(self): self._d={}
        def set(self,k,v): self._d[k]=v
        def get(self,k): return self._d.get(k)

    from app import storage
    monkeypatch.setattr(storage, "get_client", lambda: FakeRedis())

    resp = client.post("/shorten", json={"url":"https://example.com"})
    assert resp.status_code == 200
    code = resp.json()["code"]

    r = client.get(f"/{code}", allow_redirects=False)
    assert r.status_code == 307
    assert r.headers["location"] == "https://example.com"
