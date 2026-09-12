import re
import math
from fastapi import HTTPException

from config import stop_words, vectorizer, modelos
from schemas import ClasificacionResponse

def limpiar(texto: str) -> str:
    texto = texto.lower()
    texto = re.sub(r"[^a-záéíóúüñ0-9\s]", "", texto)
    tokens = texto.split()
    tokens = [t for t in tokens if t not in stop_words and len(t) > 1]

    return " ".join(tokens)

def clasificar(mensaje: str, modelo_nombre: str) -> ClasificacionResponse:
    if not mensaje.strip():
        raise HTTPException(400, "El mensaje no puede estar vacío")

    if len(mensaje) > 5000:
        raise HTTPException(400, "El mensaje es demasiado largo")

    modelo = modelos.get(modelo_nombre)

    if modelo is None:
        raise HTTPException(400, f"Modelo no válido: {modelo_nombre}")

    limpio = limpiar(mensaje)

    vector = vectorizer.transform([limpio])

    pred = modelo.predict(vector)[0]

    if hasattr(modelo, "predict_proba"):

        prob = modelo.predict_proba(vector)[0]

        conf = float(
            prob[1] if pred == 1 else prob[0]
        )
    else:
        d = modelo.decision_function(vector)[0]

        d = max(min(d, 100), -100)

        prob = 1 / (1 + math.exp(-d))

        conf = float(
            prob if pred == 1 else 1 - prob
        )

    return ClasificacionResponse(
        prediccion=int(pred),
        etiqueta="spam" if pred == 1 else "ham",
        confianza=round(conf * 100, 1),
    )
