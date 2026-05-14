# Clasificador de Spam

Proyecto de machine learning en Python para detectar mensajes spam. Entrenado con el dataset [synthetic-spam-detection-dataset-spanish](https://huggingface.co/datasets/tanaos/synthetic-spam-detection-dataset-spanish)
(15,016 mensajes en español, generados sintéticamente).

## Instalación

```bash
pip install -r requirements.txt
```

## Estructura del proyecto

```
clasificador-spam/
├── data/
│   └── spam_dataset.csv                  # 15,016 mensajes en español
├── notebook/
│   ├── notes/                            # Investigacion: tokenizacion, TF-IDF, etc.
│   ├── distribucion_clases.png           # Grafico: distribucion spam/ham
│   ├── histograma_longitud.png           # Grafico: longitudes de mensajes
│   └── nubes_palabras.png                # Grafico: nubes de palabras
├── src/
│   ├── explorar.py                       # Analisis exploratorio de datos
│   ├── descargar_datos.py                # Descarga el dataset desde Hugging Face
│   └── main.py                           # Punto de entrada
├── requirements.txt
└── README.md
```

## Pipeline

|#|Fichero|Descripcion|
|:---|:---|:---|
|1|`src/explorar.py`|Carga el dataset, distribucion y longitud de mensajes, nubes de palabras.|