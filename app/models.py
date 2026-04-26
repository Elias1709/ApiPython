from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class Lead(BaseModel):
    nombre: str
    email: EmailStr
    telefono: Optional[str] = None
    fuente: str
    producto_interes: Optional[str] = None
    presupuesto: Optional[float] = None
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()

class LeadFilter(BaseModel):    
    fuente: str | None = None
    fecha_inicio: str | None = None     # formato YYYY-MM-DD
    fecha_fin: str | None = None        # formato YYYY-MM-DD