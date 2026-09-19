"""FastAPI web application — the read-only mission-control dashboard + JSON API.

Thin wrapper over the pure renderers and the service layer. FastAPI is imported inside
`create_app` so the rest of the platform never depends on it. Auth is HTTP Basic from
EC_ADMIN_USERNAME / EC_ADMIN_PASSWORD.

Run: uvicorn everlasting_compliance.web.app:app  (or `python -m everlasting_compliance.web.app`)
"""

from __future__ import annotations

import os
import secrets

from ..db import DB
from .. import service
from ..registers import RegisterService
from ..policies import PolicyService
from .dashboard import render_dashboard


def _snapshot(db: DB) -> tuple[dict, dict, dict]:
    service.refresh_statuses(db)
    return (service.audit_readiness(db),
            RegisterService(db).health(),
            PolicyService(db).status())


def create_app():
    from fastapi import Depends, FastAPI, HTTPException, status
    from fastapi.responses import HTMLResponse, JSONResponse
    from fastapi.security import HTTPBasic, HTTPBasicCredentials

    app = FastAPI(title="Everlasting Care Compliance", docs_url=None, redoc_url=None)
    security = HTTPBasic()

    def require_auth(creds: HTTPBasicCredentials = Depends(security)) -> str:
        user = os.environ.get("EC_ADMIN_USERNAME", "admin")
        pw = os.environ.get("EC_ADMIN_PASSWORD", "")
        ok_user = secrets.compare_digest(creds.username, user)
        ok_pw = bool(pw) and secrets.compare_digest(creds.password, pw)
        if not (ok_user and ok_pw):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Unauthorized", headers={"WWW-Authenticate": "Basic"})
        return creds.username

    @app.get("/healthz")
    def healthz():
        return {"ok": True}

    @app.get("/", response_class=HTMLResponse)
    def dashboard(_: str = Depends(require_auth)):
        db = DB()  # fresh connection per request — SQLite is thread-bound
        try:
            readiness, reg, pol = _snapshot(db)
            return HTMLResponse(render_dashboard(readiness, reg, pol))
        finally:
            db.close()

    @app.get("/api/status")
    def api_status(_: str = Depends(require_auth)):
        db = DB()
        try:
            readiness, reg, pol = _snapshot(db)
            return JSONResponse({"readiness": readiness, "registers": reg, "policies": pol})
        finally:
            db.close()

    return app


# Module-level app for `uvicorn everlasting_compliance.web.app:app`.
try:  # pragma: no cover - only when fastapi is installed
    app = create_app()
except Exception:  # noqa: BLE001
    app = None


if __name__ == "__main__":  # pragma: no cover
    import uvicorn

    uvicorn.run("everlasting_compliance.web.app:app",
                host=os.environ.get("EC_DASHBOARD_HOST", "0.0.0.0"),
                port=int(os.environ.get("EC_DASHBOARD_PORT", "8080")))
