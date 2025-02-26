from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/src/main.py', methods=['POST'])
def handle_request():
    try:
        # Récupérer les données JSON envoyées par le JavaScript
        data = request.get_json()
        client_name = data.get('clientName', None)  # Récupère la valeur clientName

        # Afficher la valeur reçue dans le terminal
        print(f"Client Name reçu : {client_name}")

        # Répondre avec un message
        return jsonify({'message': 'Fichier généré avec succès.'})
    except Exception as e:
        print(f"Erreur : {e}")
        return jsonify({'message': 'Erreur lors de la génération du fichier.'})

if __name__ == '__main__':
    app.run(debug=True)