from fastapi import Depends, FastAPI

from .auth import verify_api_key
from .routes.rtds import router as rtds_router
from .routes.users import router as users_router
from .routes.workers import router as workers_router


app = FastAPI(
    title="Mock-WS API",
    version="1.0.0",
)


@app.get("/api")
async def api_root(
    _: None = Depends(verify_api_key),
):
    return {
        "message": "Mock-WS API is running"
    }


app.include_router(users_router)
app.include_router(rtds_router)
app.include_router(workers_router)