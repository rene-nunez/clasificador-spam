# Clasificador de Spam

Modelo de machine learning en Python para detectar mensajes spam. Entrenado con el dataset [synthetic-spam-detection-dataset-spanish](https://huggingface.co/datasets/tanaos/synthetic-spam-detection-dataset-spanish)
(15,016 mensajes en español, generados sintéticamente).

## Instalación

```bash
pip install -r requirements.txt
```

## Instrucciones de uso

Ejecutar el pipeline completo (pasos 1 a 6):

```bash
python src/main.py
```

Predecir mensajes propios despues del pipeline:

```bash
python src/prediccion.py
```

## Pipeline

|#|Fichero|Descripcion|
|:---|:---|:---|
|0|`src/main.py`|Orquestador: ejecuta el pipeline completo automaticamente|
|1|`src/explorar.py`|Analisis exploratorio: distribucion, longitudes, nubes de palabras|
|2|`src/limpiar.py`|Limpieza de texto: elimina duplicados, stopwords, puntuacion, minusculas|
|3|`src/balance.py`|Division 80/20 en train y test con stratify|
|4|`src/vectorizar.py`|Convierte texto a vectores TF-IDF, guarda el vectorizador|
|5|`src/entrenar.py`|Entrena Naive Bayes, Regresion Logistica y SVM, guarda los modelos|
|6|`src/evaluar.py`|Matriz de confusion, precision, recall, F1-score y analisis de errores|
|7|`src/prediccion.py`|Clasifica mensajes escritos por el usuario en tiempo real|

## Contenido

```
clasificador-spam/
├── data/
│   ├── spam_dataset.csv              # 15,016 mensajes originales
│   ├── spam_limpio.csv               # 14,750 mensajes limpios (sin duplicados)
│   ├── train.csv                     # 11,800 mensajes para entrenar
│   └── test.csv                      # 2,950 mensajes para evaluar
├── models/
│   ├── vectorizer.pkl                # Vectorizador TF-IDF entrenado
│   ├── naive_bayes.pkl               # Modelo Naive Bayes entrenado
│   ├── regresion_logistica.pkl       # Modelo Regresion Logistica entrenado
│   └── svm.pkl                       # Modelo SVM entrenado
├── notebook/
│   ├── notes/                        # Investigacion: tokenizacion, TF-IDF, etc.
│   ├── distribucion_clases.png       # Grafico: distribucion spam/ham
│   ├── histograma_longitud.png       # Grafico: longitudes de mensajes
│   └── nubes_palabras.png            # Grafico: nubes de palabras
├── src/
│   ├── balance.py                    # Division 80/20 en train y test
│   ├── descargar_datos.py            # Descarga el dataset desde Hugging Face   
│   ├── entrenar.py                   # Entrena modelos Naive Bayes, Regresion Logistica y SVM  
│   ├── evaluar.py                    # Evaluacion: matriz de confusion, precision, recall, F1
│   ├── explorar.py                   # Analisis exploratorio de datos
│   ├── limpiar.py                    # Limpieza de texto: duplicados, stopwords, puntuacion
│   ├── main.py                       # Punto de entrada (orquestador)
│   ├── prediccion.py                 # Clasifica mensajes nuevos en tiempo real
│   └── vectorizar.py                 # Convierte texto a vectores numericos (TF-IDF)
├── .gitignore
├── LICENSE.md
├── README.md
└── requirements.txt
```

## Licencia

Distribuido bajo licencia MIT. Consulta [LICENSE](LICENSE.md) para mas información.