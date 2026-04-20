from fastapi import FastAPI

app = FastAPI(
    title="Backend API",
    description="API para gestión de leads con IA",
    version="1.0.0"
)

@app.get("/")
def root():
    return {"message": "Backend API funcionando"}
