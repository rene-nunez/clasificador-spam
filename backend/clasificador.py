"""
Servicios de limpieza y clasificación de texto

Contiene:
- limpiar(): normaliza y filtra el texto para NLP.
- clasificar(): orquesta la pipeline completa de ML.
"""

import re
import math
from fastapi import HTTPException

from config import stop_words, vectorizer, modelos
from schemas import ClasificacionResponse

def limpiar(texto: str) -> str:
    """
    Limpia y normaliza un mensaje para su procesamiento NLP.

    Pasos:
    1. Convierte a minúsculas
    2. Elimina caracteres especiales
    3. Divide en tokens
    4. Elimina stopwords
    5. Elimina palabras muy cortas
    """

    texto = texto.lower()
    texto = re.sub(r"[^a-záéíóúüñ0-9\s]", "", texto)
    tokens = texto.split()
    tokens = [t for t in tokens if t not in stop_words and len(t) > 1]

    # Texto limpio para vectorización
    return " ".join(tokens)

def clasificar(mensaje: str, modelo_nombre: str) -> ClasificacionResponse:
    """
    Clasifica un mensaje como spam o ham.

    Flujo:
    1. Validar entrada
    2. Limpiar texto
    3. Vectorizar texto
    4. Ejecutar inferencia ML
    5. Calcular confianza
    6. Devolver resultado

    Argumento:
        mensaje: texto a clasificar.
        modelo_nombre: nombre del modelo ML a utilizar.

    Return:
        ClasificacionResponse: resultado con predicción, etiqueta y confianza.
    """

    # 1. Validación

    # Mensaje vacío
    if not mensaje.strip():
        raise HTTPException(400, "El mensaje no puede estar vacío")

    # Longitud máxima
    if len(mensaje) > 5000:
        raise HTTPException(400, "El mensaje es demasiado largo")

    # Modelo seleccionado
    modelo = modelos.get(modelo_nombre)

    # Validar modelo
    if modelo is None:
        raise HTTPException(400, f"Modelo no válido: {modelo_nombre}")

    # 2. Preprocesamiento
    
    # Limpiar texto
    limpio = limpiar(mensaje)

    # Vectorizar texto
    vector = vectorizer.transform([limpio])

    # 3. Inferencia ML

    # Predicción: 1 = spam, 0 = ham
    pred = modelo.predict(vector)[0]

    # 4. Cálculo de confianza
    
    # Solo el modelo Naive Bayes Multinomial y Regresion Logistica soportan probabilidades
    if hasattr(modelo, "predict_proba"):

        prob = modelo.predict_proba(vector)[0]

        conf = float(
            prob[1] if pred == 1 else prob[0]
        )
    else:
        # SVM no genera probabilidades directamente. 
        # Se usa decision_function y luego una función sigmoide
        d = modelo.decision_function(vector)[0]

        # Evita overflow numérico
        d = max(min(d, 100), -100)

        prob = 1 / (1 + math.exp(-d))

        conf = float(
            prob if pred == 1 else 1 - prob
        )

    # 5. Respuesta
    return ClasificacionResponse(
        prediccion=int(pred),
        etiqueta="spam" if pred == 1 else "ham",
        confianza=round(conf * 100, 1),
    )