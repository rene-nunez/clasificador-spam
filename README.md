# Clasificador de Spam

Proyecto de machine learning en Python para detectar mensajes spam. Entrenado con el dataset [synthetic-spam-detection-dataset-spanish](https://huggingface.co/datasets/tanaos/synthetic-spam-detection-dataset-spanish)
(15,016 mensajes en español, generados sintéticamente).

## Requisitos

```bash
pip install -r requirements.txt
```

## Estructura del proyecto

```
clasificador-spam/
├── data/
│   └── spam_dataset.csv          # 15,016 mensajes en español
├── src/
│   ├── descargar_datos.py        # Descarga el dataset desde Hugging Face
│   └── main.py                   # Punto de entrada
├── requirements.txt
└── README.md
```