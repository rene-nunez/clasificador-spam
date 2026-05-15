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
│   ├── spam_dataset.csv                  # 15,016 mensajes originales
│   ├── spam_limpio.csv                   # 14,750 mensajes limpios (sin duplicados)
│   ├── train.csv                         # 11,800 mensajes para entrenar
│   └── test.csv                          # 2,950 mensajes para evaluar
├── models/
│   └── vectorizer.pkl                    # Vectorizador TF-IDF entrenado
├── notebook/
│   ├── notes/                            # Investigacion: tokenizacion, TF-IDF, etc.
│   ├── distribucion_clases.png           # Grafico: distribucion spam/ham
│   ├── histograma_longitud.png           # Grafico: longitudes de mensajes
│   └── nubes_palabras.png                # Grafico: nubes de palabras
├── src/
│   ├── balance.py                        # Division 80/20 en train y test
│   ├── descargar_datos.py                # Descarga el dataset desde Hugging Face   
│   ├── explorar.py                       # Analisis exploratorio de datos
│   ├── limpiar.py                        # Limpieza de texto: duplicados, stopwords, puntuacion
│   ├── main.py                           # Punto de entrada
│   └── vectorizar.py                     # Convierte texto a vectores numericos (TF-IDF)
├── requirements.txt
└── README.md
```

## Pipeline

|#|Fichero|Descripcion|
|:---|:---|:---|
|1|`src/explorar.py`|Analisis exploratorio: distribucion, longitudes, nubes de palabras|
|2|`src/limpiar.py`|Limpieza de texto: elimina duplicados, stopwords, puntuacion, minusculas|
|3|`src/balance.py`|Division 80/20 en train y test con stratify|
|4|`src/vectorizar.py`|Convierte texto a vectores TF-IDF, guarda el vectorizador|