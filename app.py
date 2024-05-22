from flask import Flask, request, render_template, redirect, url_for, jsonify
import re
import random

app = Flask(__name__)

# Diccionario de antónimos en español
antonyms = {
    'rápido': ['lento', 'pausado'],
    'feliz': ['triste', 'miserable', 'infeliz'],
    'grande': ['pequeño', 'minúsculo'],
    'caliente': ['frío', 'helado'],
    'lleno': ['vacío'],
    'nuevo': ['viejo', 'antiguo'],
    'duro': ['blando', 'suave'],
    'fuerte': ['débil', 'frágil'],
    'rico': ['pobre', 'necesitado'],
    'claro': ['oscuro', 'sombreado'],
    'joven': ['viejo', 'anciano'],
    'alegre': ['triste', 'apagado'],
    'subir': ['bajar', 'descender'],
    'ganar': ['perder'],
    'amor': ['odio'],
    'encender': ['apagar', 'extinguir'],
    'comenzar': ['terminar', 'finalizar'],
    'abrir': ['cerrar'],
    'mejorar': ['empeorar', 'degradar']
}

def analyze_code(code):
    tokens = []
    lines = code.split('\n')
    
    for line_number, line in enumerate(lines, start=1):
        words = re.findall(r'\b\w+\b|\S', line)
        
        for word in words:
            token = {
                'value': word,
                'antónimo': '',
                'dígito': '',
                'símbolo': '',
                'line': line_number
            }

            if word.isdigit():
                token['dígito'] = 'X'
            elif re.match(r'\W', word):
                token['símbolo'] = 'X'
            else:
                if word.lower() in antonyms:
                    token['antónimo'] = random.choice(antonyms[word.lower()])
                else:
                    token['antónimo'] = "N/A"  # Indicar que no hay antónimo disponible
            
            tokens.append(token)
    
    return tokens

@app.route('/')
def index():
    return render_template('index.html', results=None)

@app.route('/analyze', methods=['POST'])
def analyze():
    code = request.form.get('code')
    
    if not code:
        return jsonify({"error": "Por favor, ingrese texto para analizar"}), 400
    
    results = analyze_code(code)
    return render_template('index.html', results=results, code=code)

if __name__ == '__main__':
    app.run(debug=True)
