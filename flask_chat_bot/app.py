from flask import Flask, request, jsonify
import openai
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Configura el modelo de OpenAI
model_name = 'gpt-3.5-turbo'  # Reemplaza con el modelo correcto

# Lista de juegos y precios (esto debería ser una base de datos en un caso real)
juegos_precios = {
    "Fortnite": 0.00,
    "Call of Duty: Modern Warfare II": 69.99,
    "League of Legends": 0.00,
    "Valorant": 0.00,
    "Genshin Impact": 0.00,
    "Apex Legends": 0.00,
    "Minecraft": 26.95,
    "Roblox": 0.00,
    "The Legend of Zelda: Tears of the Kingdom": 69.99,
    "FIFA 24": 59.99,
    "Cyberpunk 2077": 29.99,
    "Animal Crossing: New Horizons": 59.99,
    "Among Us": 4.99,
    "The Witcher 3: Wild Hunt": 39.99,
    "Super Mario Odyssey": 59.99,
    "Assassin's Creed: Valhalla": 49.99,
    "DoomEternal": 39.99,
    "World of Warcraft: Shadowlands": 49.99,
    "Final Fantasy XIV": 39.99,
    "Pokémon Brilliant Diamond/Shining Pearl": 59.99,
    "Overwatch 2": 59.99,
    "Star Wars Jedi: Fallen Order": 49.99,
    "Rainbow Six Siege": 19.99,
    "Monster Hunter Rise": 59.99,
    "Death Stranding Director's Cut": 49.99,
    "The Elder Scrolls V: Skyrim Anniversary Edition": 59.99,
    "Halo Infinite": 59.99,
    "Splatoon 3": 59.99,
    "Metroid Prime 4": 69.99,
    "The Last of Us Part II": 49.99,
    "Battlefield 2042": 59.99,
    "Ghost of Tsushima": 49.99,
    "Far Cry 6": 59.99,
    "Hitman 3": 59.99,
    "Resident Evil Village": 49.99,
    "God of WarRagnarök": 69.99,
    "Cyber Shadow": 19.99,
    "Dark Souls III": 59.99,
    "Devil May Cry 5": 39.99
}

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    prompt = data.get('prompt')
    
    if not prompt:
        return jsonify({'error': 'No prompt provided'}), 400

    try:
        response = openai.ChatCompletion.create(
            model=model_name,
            messages=[
                {"role": "system", "content": "Eres un asistente que se encarga de ofrecer información sobre los juegos que vende la tienda Pixel Plax"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150
        )
        openai_response = response['choices'][0]['message']['content'].strip()

        # Buscar en la lista de juegos
        juego_solicitado = None
        for juego in juegos_precios:
            if juego.lower() in prompt.lower():
                juego_solicitado = juego
                break
        
        if juego_solicitado:
            precio = juegos_precios[juego_solicitado]
            return jsonify({'response': f'El precio de {juego_solicitado} es ${precio:.2f}'})
        else:
            return jsonify({'response': openai_response})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    if not openai.api_key:
        raise ValueError("No API key found. Set the OPENAI_API_KEY environment variable.")
    
    app.run(host='0.0.0.0', port=5000)
