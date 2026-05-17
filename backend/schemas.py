"""
Modelos de datos Pydantic para la API

Definen la estructura de las peticiones y respuestas
de los endpoints de clasificación.
"""

# Validación de datos JSON mediante Pydantic
from pydantic import BaseModel

# Petición
class MensajeRequest(BaseModel):
    mensaje: str # Texto a clasificar
    modelo: str = "Regresión Logística" # Nombre del modelo ML por defecto

# Respuesta
class ClasificacionResponse(BaseModel):
    prediccion: int # 1 = spam, 0 = ham
    etiqueta: str # "spam" o "ham"
    confianza: float # Porcentaje de confianza (0–100)