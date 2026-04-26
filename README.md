# ApiPython
Backend con FastAPI y MongoDB

# API de Leads con Resumen Ejecutivo

## 1. INSTALACIÓN
```bash
git clone https://github.com/Elias1709/ApiPython.git
cd ApiPython
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
pip install -r requirements.txt

Enlace inicial de API: http://127.0.0.1:8000/docs

## 2. TECNOLOGIAS USADAS
## FastAPI — rapidez y documentación automática

## MongoDB — almacenamiento flexible de leads

## OpenAI API — generación de resúmenes ejecutivos

## Uvicorn — servidor ASGI

## 3. SEED DE DATOS

## Para llenar la base de datos, Ejecutar el comando de abajo
python seed.py

## 4. EJEMPLOS DE ENDPOINTS

## Obtener token
curl -X POST "http://127.0.0.1:8000/token" \
     -d "username=admin&password=1234"

## Crear lead
curl -X POST "http://127.0.0.1:8000/leads" \
     -H "Authorization: Bearer <token>" \
     -H "Content-Type: application/json" \
     -d '{"nombre":"Juan","fuente":"instagram","fecha":"2026-04-20"}'

## Resumen ejecutivo de leads
curl -X POST "http://127.0.0.1:8000/leads/ai/summary" \
     -H "Authorization: Bearer <token>" \
     -H "Content-Type: application/json" \
     -d '{
       "fuente": "instagram",
       "fecha_inicio": "2026-04-20",
       "fecha_fin": "2026-04-22"
     }'

## 5. VARIABLES DE ENTORNO 
Crea un archivo .env con tus valores reales. El repo incluye .env.example como referencia:
OPENAI_API_KEY=
MONGO_URI=
SECRET_KEY=

## 6. MANEJO DE ERRORES
La API devuelve errores usando HTTPException. Ejemplo:

{
  "detail": "No se encontraron leads con ese filtro"
}
