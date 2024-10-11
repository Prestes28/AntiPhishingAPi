import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import joblib
import nltk
from nltk.corpus import stopwords

# Descargar stopwords de NLTK
nltk.download('stopwords')

# Cargar el dataset
df = pd.read_csv('phishing_email.csv')  # Ruta al dataset descargado
# Supongamos que el dataset tiene las columnas 'text' (contenido del email) y 'label' (0: no phishing, 1: phishing)
print(df.columns)

# Preprocesamiento de texto
stop_words = stopwords.words('english')
tfidf = TfidfVectorizer(stop_words=stop_words)

# Transformar los textos en vectores TF-IDF
X = tfidf.fit_transform(df['text_combined'].values)
y = df['label'].values

# Dividir el dataset en entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Entrenar un modelo básico de regresión logística
model = LogisticRegression()
model.fit(X_train, y_train)

# Evaluar el modelo
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy}')

# Guardar el modelo y el vectorizador para usarlos en la API
joblib.dump(model, 'phishing_model.pkl')
joblib.dump(tfidf, 'tfidf_vectorizer.pkl')
