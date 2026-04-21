from pydantic import BaseModel, EmailStr
from typing import Optional

class Lead(BaseModel):
    nombre: str
    email: EmailStr
    telefono: Optional[str] = None
    fuente: str
    producto_interes: Optional[str] = None
    presupuesto: Optional[float] = None
