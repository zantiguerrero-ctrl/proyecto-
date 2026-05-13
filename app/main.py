from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import router

app = FastAPI(
    title="DiagnoHealth API",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rutas
app.include_router(router)

# Ruta principal
@app.get("/")
def home():
    return {
        "message": "DiagnoHealth API funcionando"
    }
