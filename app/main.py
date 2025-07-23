from fastapi import FastAPI
from app.api import resume_router

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Resume Screening API is live 🚀"}

app.include_router(resume_router.router, prefix="/resume")
