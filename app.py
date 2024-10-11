from flask import Flask, request, jsonify, render_template
import joblib
import numpy as np
import nltk
from nltk.corpus import stopwords
from googletrans import Translator

# Descargar stopwords de NLTK
nltk.download('stopwords')

# Crear una instancia de la aplicación Flask
app = Flask(__name__)

# Cargar el modelo y el vectorizador
model = joblib.load('phishing_model.pkl')
tfidf_vectorizer = joblib.load('tfidf_vectorizer.pkl')

# Función para preprocesar el texto del correo
def preprocess_email(text):
    stop_words = stopwords.words('english')
    # Transformar el texto en vector TF-IDF
    processed_text = tfidf_vectorizer.transform([text])
    return processed_text

translator = Translator()

# Ruta para mostrar la interfaz gráfica
@app.route('/')
def index():
    return render_template('index.html')

# Ruta de la API para analizar un correo electrónico
@app.route('/analyze-email', methods=['POST'])
def analyze_email():
    try:
        # Obtener el texto del correo electrónico
        email_text = request.json['email_text']
        
        # Traducir el texto al inglés antes de procesarlo
        email_text_translated = translator.translate(email_text, src='es', dest='en')
        
        # Preprocesar el texto traducido
        processed_email = preprocess_email(email_text_translated.text)
        
        # Hacer una predicción usando el modelo entrenado
        prediction = model.predict(processed_email)
        
        # Construir la respuesta basada en la predicción
        if prediction[0] == 1:
            result = "Phishing detectado"  # Respuesta en español
        else:
            result = "El correo es seguro"  # Respuesta en español
        
        # Responder con el resultado en español
        return jsonify({'result': result})
    
    except KeyError:
        return jsonify({'error': 'Entrada inválida, proporcione el campo "email_text"'}), 400

if __name__ == '__main__':
    app.run(debug=True)
