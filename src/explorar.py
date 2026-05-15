"""
Análisis exploratorio del dataset de spam

Este script carga el dataset y nos ayuda a entender cómo son los datos 
antes de empezar a limpiarlos y entrenar modelos.
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

# Obtener la ruta base del proyecto (subiendo desde src/ hasta la raiz)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 1. Cargar datos
ruta_csv = os.path.join(BASE_DIR, "data", "spam_dataset.csv")
df = pd.read_csv(ruta_csv)

print("Análisis exploratorio del dataset")

print(f"\nDimensiones: {df.shape[0]} filas, {df.shape[1]} columnas")
print(f"Columnas: {list(df.columns)}")

print("-" * 30)

# 2. Distribución de clases
print("\nDistribución de clases")
print(df["label"].value_counts())
print(f"\nPorcentajes:")
print(df["label"].value_counts(normalize=True).mul(100).round(1).astype(str) + "%")

# Creación del gráfico de barras
plt.figure(figsize=(6, 4))
sns.countplot(data=df, x="label", hue="label", palette={"ham": "green", "spam": "red"}, legend=False)
plt.title("Distribución de clases: Ham vs Spam")
plt.xlabel("Clase")
plt.ylabel("Cantidad")
plt.tight_layout()
plt.savefig(os.path.join(BASE_DIR, "notebook", "distribucion_clases.png"))
print("\nGráfico creado: notebook/distribucion_clases.png")

print("-" * 30)

# 3. Longitud de los mensajes
df["longitud"] = df["mensaje"].str.len()

print("\nEstadísticas de longitud (caracteres)")
print(df.groupby("label")["longitud"].describe().round(1))

# Creación del histograma comparativo
plt.figure(figsize=(10, 5))
for clase, color in [("ham", "green"), ("spam", "red")]:
    subset = df[df["label"] == clase]["longitud"]
    plt.hist(subset, bins=50, alpha=0.5, label=clase, color=color)
plt.title("Distribución de longitud de mensajes")
plt.xlabel("Cantidad de caracteres")
plt.ylabel("Frecuencia")
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(BASE_DIR, "notebook", "histograma_longitud.png"))
print("Gráfico creado: notebook/histograma_longitud.png")

print("-" * 30)

# 4. Nubes de palabras por clase
print("\nNubes de palabras por clase")

# Unimos todos los mensajes de cada clase en un solo texto
texto_ham = " ".join(df[df["label"] == "ham"]["mensaje"])
texto_spam = " ".join(df[df["label"] == "spam"]["mensaje"])

# Creación de la nube de palabras para ham
plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
nube_ham = WordCloud(width=400, height=300, background_color="white", colormap="Greens").generate(texto_ham)
plt.imshow(nube_ham, interpolation="bilinear")
plt.axis("off")
plt.title("Palabras ham más frecuentes")

# Creación de la nube de palabras para spam
plt.subplot(1, 2, 2)
nube_spam = WordCloud(width=400, height=300, background_color="white", colormap="Reds").generate(texto_spam)
plt.imshow(nube_spam, interpolation="bilinear")
plt.axis("off")
plt.title("Palabras spam más frecuentes")

plt.tight_layout()
plt.savefig(os.path.join(BASE_DIR, "notebook", "nubes_palabras.png"))
print("Gráfico creado: notebook/nubes_palabras.png")

print("-" * 30)

# 5. Mostrar ejemplos
print("\nEjemplos de ham")
print(df[df["label"] == "ham"]["mensaje"].iloc[:5].to_string(index=False))

print("\nEjemplos de spam")
print(df[df["label"] == "spam"]["mensaje"].iloc[:5].to_string(index=False))

print("-" * 30)

# 6. Datos faltantes y duplicados
print(f"\nCalidad de datos")
print(f"Valores nulos: {df.isnull().sum().sum()}")
duplicados = df.duplicated(subset=["mensaje"]).sum()
print(f"Mensajes duplicados: {duplicados} ({duplicados/len(df)*100:.1f}%)")

print("-" * 30)
print("\nResumen del analisis:")
print(f"  - Dataset balanceado: {df['label'].value_counts(normalize=True).mul(100).round(1).to_dict()}")
print(f"  - Spam ligeramente mas largo: ~85 caracteres promedio vs ~74 en ham")
print(f"  - Vocabulario distinto entre clases (visible en nubes de palabras)")
print(f"\nAnalisis completado. Revisa los graficos en la carpeta notebook/")