"""
Clasificador de Spam

Ejecuta todo el proceso desde la exploracion hasta la prediccion (pipeline completo).
"""

import os
import subprocess
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS = [
    ("Exploracion de datos", "explorar.py"),
    ("Limpieza de texto", "limpiar.py"),
    ("Division train/test", "balance.py"),
    ("Vectorizacion TF-IDF", "vectorizar.py"),
    ("Entrenamiento de modelos", "entrenar.py"),
    ("Evaluacion de modelos", "evaluar.py"),
]
print("-" * 30)
print("Clasificador de Spam")
print("-" * 30)

for paso, (nombre, script) in enumerate(SCRIPTS, 1):
    print(f"\nPaso {paso}/{len(SCRIPTS)}: {nombre}")
    ruta = os.path.join(BASE_DIR, "src", script)
    resultado = subprocess.run([sys.executable, ruta], capture_output=True, text=True)
    print(resultado.stdout)

    if resultado.returncode != 0:
        print(f"Error en paso {paso} ({nombre}):")
        print(resultado.stderr)
        sys.exit(1)

print("\n" + "-" * 30)
print("Pipeline completado exitosamente.")
print("-" * 30)