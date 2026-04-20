from fastapi import FastAPI
from app.models import Lead
from app.config import db
from fastapi import FastAPI, HTTPException


app = FastAPI(
    title="Backend API",
    description="API para gestión de leads con IA",
    version="1.0.0"
)

@app.get("/")
def root():
    return {"message": "Backend API funcionando"}

""" @app.post("/leads")
def create_lead(lead: Lead):
    result = db.leads.insert_one(lead.dict())
    return {"id": str(result.inserted_id), "message": "Lead registrado exitosamente"} """

@app.post("/leads")
def create_lead(lead: Lead):
    if db.leads.find_one({"email": lead.email}):
        raise HTTPException(status_code=400, detail="El email ya está registrado")

    result = db.leads.insert_one(lead.dict())
    return {"id": str(result.inserted_id), "message": "Lead registrado exitosamente"}

@app.get("/leads")
def get_leads():
    leads = list(db.leads.find({}, {"_id": 0}))
    return {"leads": leads}

@app.get("/leads/{email}")
def get_lead(email: str):
    lead = db.leads.find_one({"email": email}, {"_id": 0})
    if not lead:
        raise HTTPException(status_code=404, detail="Lead no encontrado")
    return lead

@app.put("/leads/{email}")
def update_lead(email: str, lead: Lead):
    result = db.leads.update_one({"email": email}, {"$set": lead.dict()})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Lead no encontrado")
    return {"message": "Lead actualizado exitosamente"}

@app.delete("/leads/{email}")
def delete_lead(email: str):
    result = db.leads.delete_one({"email": email})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Lead no encontrado")
    return {"message": "Lead eliminado exitosamente"}


