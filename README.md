# Clasificador de Spam

Modelos de machine learning en Python para detectar mensajes spam. Entrenados con el dataset [synthetic-spam-detection-dataset-spanish](https://huggingface.co/datasets/tanaos/synthetic-spam-detection-dataset-spanish) (15,016 mensajes en español, generados sintéticamente).

## Licencia

Distribuido bajo licencia MIT. El dataset también se distribuye bajo MIT, y los archivos generados a partir de él (`data/`, `models/`) heredan la misma licencia. Consulta [LICENSE](LICENSE.md) para más información.

## Instalación

```bash
pip install -r requirements.txt
cd frontend && npm install
```

## Instrucciones de uso

### Pipeline completo (entrenar modelos)

```bash
python src/main.py
```

### Clasificar desde terminal

```bash
python src/prediccion.py
```

### Interfaz web (un solo comando)

Primero construir el frontend (solo una vez, o al cambiar archivos del frontend):

```bash
cd frontend && npm run build
```

Luego iniciar el backend (sirve la API y el frontend estático juntos):

```bash
python backend/api.py
```

Abrir [http://localhost:8000](http://localhost:8000).

Si existe `frontend/dist/` (el build), la raíz muestra la app web. Si no, redirige a `/docs`.

### Interfaz web (desarrollo con HMR)

Otra forma de ejecutar el programa si no se construye un dist del frontend con vite es la siguiente:

```bash
# Terminal 1 (reload activo)
cd backend && uvicorn api:app --reload

# Terminal 2 — frontend (HMR al editar archivos)
cd frontend && npm run dev
```

Abrir [http://localhost:3000](http://localhost:3000).

### Documentación interactiva (Swagger)

Con el backend corriendo, la API expone documentación automática:

- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## Pipeline de entrenamiento (`src/`)

|#|Script|Descripción|
|:---|:---|:---|
|0|`src/main.py`|Orquestador del pipeline completo|
|1|`src/descargar_datos.py`|Descarga el dataset desde Hugging Face|
|2|`src/explorar.py`|Análisis exploratorio: distribución, longitudes, nubes de palabras|
|3|`src/limpiar.py`|Limpieza: duplicados, stopwords, puntuación, minúsculas|
|4|`src/balance.py`|División 80/20 en train/test con stratify|
|5|`src/vectorizar.py`|Convierte texto a vectores TF-IDF|
|6|`src/entrenar.py`|Entrena Naive Bayes, Regresión Logística y SVM|
|7|`src/evaluar.py`|Matriz de confusión, precisión, recall, F1-score|
|8|`src/prediccion.py`|Clasifica mensajes escritos por el usuario en tiempo real|

> [!NOTE]
> Los scripts en `src/` son el pipeline de entrenamiento.
> La **API** que sirve las predicciones web está en `backend/`.
> No confundir `src/main.py` (orquestador de entrenamiento) con `backend/api.py` (servidor FastAPI).