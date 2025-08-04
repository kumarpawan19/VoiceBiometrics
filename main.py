from fastapi import FastAPI
from app.routes.auth_routes import router as auth_router
from app.routes.phrase_routes import router as phrase_router

app = FastAPI()

@app.get("/health")
def health_check():
    return {"status": "ok"}

# Include Routers
app.include_router(phrase_router, prefix="/phrase", tags=["Liveness"])
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])

