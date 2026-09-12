"""
    clasificador-spam: Modelos para clasificar mensajes de spam en español
    Copyright (C) 2026 René Núñez

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import os
import subprocess
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS = [
    ("Descarga de datos", "descargar_datos.py"),
    ("Exploracion de datos", "explorar.py"),
    ("Limpieza de texto", "limpiar.py"),
    ("Division train/test", "balance.py"),
    ("Vectorizacion TF-IDF", "vectorizar.py"),
    ("Entrenamiento de modelos", "entrenar.py"),
    ("Evaluacion de modelos", "evaluar.py"),
]

if __name__ == "__main__":
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
