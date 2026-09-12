import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    train = pd.read_csv(os.path.join(BASE_DIR, "data", "train.csv"))
    test = pd.read_csv(os.path.join(BASE_DIR, "data", "test.csv"))

    train["mensaje_limpio"] = train["mensaje_limpio"].fillna("")
    test["mensaje_limpio"] = test["mensaje_limpio"].fillna("")

    print(f"Train: {len(train)} mensajes")
    print(f"Test: {len(test)} mensajes")

    vectorizer = TfidfVectorizer(max_df=0.95, min_df=2, ngram_range=(1, 2))

    X_train = vectorizer.fit_transform(train["mensaje_limpio"])

    X_test = vectorizer.transform(test["mensaje_limpio"])

    y_train = train["spam"]
    y_test = test["spam"]

    print(f"\nVocabulario aprendido: {len(vectorizer.get_feature_names_out())} palabras")
    print(f"Train vectorizado: {X_train.shape}")
    print(f"Test vectorizado: {X_test.shape}")

    models_dir = os.path.join(BASE_DIR, "models")
    os.makedirs(models_dir, exist_ok=True)

    joblib.dump(vectorizer, os.path.join(models_dir, "vectorizer.pkl"))
    print(f"\nVectorizador guardado: models/vectorizer.pkl")
