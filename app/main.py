from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.models import Lead
from app.config import db
from app.auth import create_access_token, verify_token


app = FastAPI(
    title="Backend API",
    description="API para gestión de leads con IA",
    version="1.0.0"
)

@app.get("/")
def root():
    return {"message": "Backend API funcionando"}

@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Aquí deberías validar usuario/contraseña contra tu base de datos
    if form_data.username != "admin" or form_data.password != "1234":
        raise HTTPException(status_code=400, detail="Credenciales inválidas")
    access_token = create_access_token(data={"sub": form_data.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/leads")
def create_lead(lead: Lead, token: dict = Depends(verify_token)):
    if db.leads.find_one({"email": lead.email}):
        raise HTTPException(status_code=400, detail="El email ya está registrado")
    result = db.leads.insert_one(lead.model_dump())
    return {"id": str(result.inserted_id), "message": "Lead registrado exitosamente"}

@app.get("/leads")
def get_leads(token: dict = Depends(verify_token)):
    leads = list(db.leads.find({}, {"_id": 0}))
    return {"leads": leads}

@app.get("/leads/{email}")
def get_lead(email: str, token: dict = Depends(verify_token)):
    lead = db.leads.find_one({"email": email}, {"_id": 0})
    if not lead:
        raise HTTPException(status_code=404, detail="Lead no encontrado")
    return lead

@app.put("/leads/{email}")
def update_lead(email: str, lead: Lead, token: dict = Depends(verify_token)):
    result = db.leads.update_one({"email": email}, {"$set": lead.model_dump()})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Lead no encontrado")
    return {"message": "Lead actualizado exitosamente"}

@app.delete("/leads/{email}")
def delete_lead(email: str, token: dict = Depends(verify_token)):
    result = db.leads.delete_one({"email": email})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Lead no encontrado")
    return {"message": "Lead eliminado exitosamente"}


