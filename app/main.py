import os
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from bson import ObjectId
from datetime import datetime, timedelta
from openai import OpenAI
from app.models import Lead
from app.models import LeadFilter
from app.config import db
from app.auth import create_access_token, verify_token

##client_ai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
api_key = os.getenv("OPENAI_API_KEY")
client_ai = OpenAI(api_key=api_key) if api_key else None

class LeadFilter(BaseModel):
    fuente: str | None = None
    fecha_inicio: str | None = None
    fecha_fin: str | None = None

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
def list_leads(page: int = 1, limit: int = 10, fuente: str | None = None,
               fecha_inicio: str | None = None, fecha_fin: str | None = None,
               token: dict = Depends(verify_token)):
    query = {}
    if fuente:
        query["fuente"] = fuente
    if fecha_inicio and fecha_fin:
        query["created_at"] = {"$gte": fecha_inicio, "$lte": fecha_fin}

    cursor = (
        db.leads.find(query)
        .skip((page - 1) * limit)
        .limit(limit)
        .sort("created_at", -1)
    )

    leads = []
    for lead in cursor:
        lead["_id"] = str(lead["_id"]) 
        leads.append(lead)

    return {"leads": leads}

@app.post("/leads/stats")
def leads_stats(filtro: LeadFilter, token: dict = Depends(verify_token)):
    query = {}
    if filtro.fuente:
        query["fuente"] = filtro.fuente
    if filtro.fecha_inicio and filtro.fecha_fin:
        try:
            fi = datetime.strptime(filtro.fecha_inicio, "%Y-%m-%d")
            ff = datetime.strptime(filtro.fecha_fin, "%Y-%m-%d")
            query["fecha"] = {"$gte": fi, "$lte": ff}
        except ValueError:
            raise HTTPException(status_code=400, detail="Formato de fecha inválido, usa YYYY-MM-DD")

    try:
        total = db.leads.count_documents(query)
        por_fuente = list(db.leads.aggregate([
            {"$match": query},
            {"$group": {"_id": "$fuente", "count": {"$sum": 1}}}
        ]))
        por_fuente_dict = {str(item["_id"]) if item["_id"] else "Sin fuente": item["count"] for item in por_fuente}

        return {
            "total_leads": total,
            "por_fuente": por_fuente_dict
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generando estadísticas: {str(e)}")
    
@app.get("/leads/{id}")
def get_lead(id: str, token: dict = Depends(verify_token)):
    lead = db.leads.find_one({"_id": ObjectId(id)}, {"_id": 0})
    if not lead:
        raise HTTPException(status_code=404, detail="Lead no encontrado")
    return lead

@app.patch("/leads/{id}")
def update_lead(id: str, lead_update: dict, token: dict = Depends(verify_token)):
    result = db.leads.update_one({"_id": ObjectId(id)}, {"$set": lead_update})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Lead no encontrado")
    return {"message": "Lead actualizado exitosamente"}

@app.delete("/leads/{id}")
def delete_lead(id: str, token: dict = Depends(verify_token)):
    result = db.leads.update_one({"_id": ObjectId(id)}, {"$set": {"deleted": True}})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Lead no encontrado")
    return {"message": "Lead eliminado (soft delete)"}

""" @app.get("/leads/stats")
def leads_stats(token: dict = Depends(verify_token)):
    try:
        total = db.leads.count_documents({})
        return {"total_leads": total}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}") """
    

@app.post("/leads/ai/summary")
def ai_summary(filtro: LeadFilter, token: dict = Depends(verify_token)):
    query = {}
    if filtro.fuente:
        query["fuente"] = filtro.fuente
    if filtro.fecha_inicio and filtro.fecha_fin:
        query["fecha"] = {"$gte": filtro.fecha_inicio, "$lte": filtro.fecha_fin}

    leads = []
    for lead in db.leads.find(query, {"_id": 0}):
        clean_lead = {k: str(v) for k, v in lead.items()}
        leads.append(clean_lead)

    if not leads:
        raise HTTPException(status_code=404, detail="No se encontraron leads con ese filtro")

    prompt = f"""
    Analiza estos leads y genera un resumen ejecutivo estructurado:
    - Número de leads: {len(leads)}
    - Datos: {leads}
    
    Devuelve el resultado en tres secciones claras:
    1. Análisis general
    2. Fuente principal
    3. Recomendaciones estratégicas
    """
    try:
        response = client_ai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Eres un analista de marketing."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300
        )
        resumen = response.choices[0].message.content.strip()
        return {"summary": resumen}
    except Exception as e:        
        resumen = f"""
        1. Análisis general: Se encontraron {len(leads)} leads.
        2. Fuente principal: {leads[0].get("fuente", "Desconocida")}.
        3. Recomendaciones estratégicas: revisar campañas y optimizar inversión.
        """
        return {"summary": resumen}