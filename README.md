# Clasificador de Spam

Modelos de machine learning para detectar mensajes spam en español. Entrenados con el dataset [synthetic-spam-detection-dataset-spanish](https://huggingface.co/datasets/tanaos/synthetic-spam-detection-dataset-spanish) (15,016 mensajes sintéticos).

## Instalación

```bash
pip install -r requirements.txt
cd frontend && npm install
```

## Instrucciones de uso

### Interfaz web (producción)

Construir el frontend y arrancar el backend (un solo proceso, mismo puerto):

```bash
cd frontend && npm run build
python backend/api.py
```

Abrir [http://localhost:8000](http://localhost:8000).

### Interfaz web (desarrollo)

Dos procesos separados con recarga automática al editar archivos:

```bash
cd backend && uvicorn api:app --reload
cd frontend && npm run dev
```

Abrir [http://localhost:3000](http://localhost:3000).

### Entrenar modelos (opcional)

Los modelos ya están pre-entrenados e incluidos en el repositorio. Solo ejecutar si se desea reentrenar:

```bash
python src/main.py
```

### Clasificar desde terminal

Alternativa a la interfaz web, desde la línea de comandos:

```bash
python src/prediccion.py
```

## Pipeline

|#|Script|Descripción|
|:---|:---|:---|
|0|`src/main.py`|Orquestador del pipeline completo|
|1|`src/descargar_datos.py`|Descarga el dataset desde Hugging Face|
|2|`src/explorar.py`|Análisis exploratorio de los datos|
|3|`src/limpiar.py`|Limpieza y normalización del texto|
|4|`src/balance.py`|División en train y test|
|5|`src/vectorizar.py`|Vectorización TF-IDF|
|6|`src/entrenar.py`|Entrenamiento de los modelos|
|7|`src/evaluar.py`|Evaluación y métricas de rendimiento|
|8|`src/prediccion.py`|Clasificación interactiva desde terminal|

## Ética y finalidad

Este proyecto tiene fines **educativos y de investigación**. Clasificar mensajes como spam o ham puede ayudar a filtrar contenido no deseado, pero también implica decisiones sobre qué se considera spam. El dataset usado es sintético y no contiene mensajes reales de usuarios, lo que elimina riesgos de privacidad. Los modelos no deben usarse para censurar contenido ni para tomar decisiones automatizadas sin supervisión humana.

## Licencia

Este proyecto y el dataset utilizado se distribuyen bajo licencia MIT. Consulta [LICENSE](./LICENSE) para más información.