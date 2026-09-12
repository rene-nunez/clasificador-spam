# Clasificador de Spam

Modelos de ML (Naive Bayes, Regresión logística y SVM) para clasificar mensajes de spam en español, entrenados con el dataset sintético [synthetic-spam-detection-dataset-spanish](https://huggingface.co/datasets/tanaos/synthetic-spam-detection-dataset-spanish) (15,016 mensajes).

## Instalación

```bash
pip install -r requirements.txt
cd frontend && npm install
```

## Instrucciones de uso

### CLI

```bash
python src/prediccion.py
```

### Interfaz web (desarrollo)

```bash
cd backend && uvicorn api:app --reload
cd frontend && npm run dev
```

Abrir http://localhost:3000.

### Interfaz web (producción)

```bash
cd frontend && npm run build
python backend/api.py
```

Abrir http://localhost:8000.

## Entrenamiento

Todos los artefactos de `data/`, `models/` y `notebook/` se generan desde cero ejecutando el pipeline completo. El entrenamiento es reproducible: la semilla aleatoria está fijada en 42, por lo que cada pipeline produce los mismos resultados. El único paso que requiere internet es la descarga del dataset.

```bash
python src/main.py
```

El pipeline descarga el dataset, analiza los datos, limpia el texto, divide en train/test, vectoriza con TF-IDF, entrena los tres modelos y los evalúa.

## API

Backend desarrollado con FastAPI en `backend/api.py`. Documentación interactiva de cada endpoint disponible en `/docs` al ejecutar el servidor.

## Licencia

Este proyecto se distribuye bajo la licencia GPLv3. Consulta [LICENSE](./LICENSE) para más información. El dataset utilizado se distribuye por separado bajo la licencia MIT.
