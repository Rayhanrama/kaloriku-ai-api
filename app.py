from flask import Flask, request, jsonify
from langchain_community.llms import Replicate
import os

app = Flask(__name__)

# Inisialisasi model Replicate (pakai Granite)
model = Replicate(
    model="ibm-granite/granite-3.3-8b-instruct",
    replicate_api_token=os.environ.get('REPLICATE_API_TOKEN'),
    model_kwargs={"max_tokens": 1024, "temperature": 0.2},
)

# Template prompt untuk diet AI
def zeroshot_prompt_diet(data):
    return f"""
    Saya pengguna aplikasi diet bernama Kaloriku. Hari ini saya telah mengonsumsi {data['kalori_masuk']}kkal dan membakar {data['kalori_terbakar']}kkal.
    Target defisit saya {data['target_defisit']}kkal. Berikan saran makanan atau aktivitas tambahan yang ringkas dan mudah dipahami.
    """

# Homepage route untuk cek server aktif
@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "status": "ok",
        "message": "✅ Flask API Kaloriku AI is running!"
    })

# Endpoint utama untuk menerima POST dari Laravel
@app.route('/saran-ai', methods=['POST'])
def saran_ai():
    try:
        data = request.get_json()

        # Validasi sederhana
        if not data or not all(k in data for k in ('kalori_masuk', 'kalori_terbakar', 'target_defisit')):
            return jsonify({'error': 'Data tidak lengkap'}), 400

        # Generate prompt dan invoke AI
        prompt = zeroshot_prompt_diet(data)
        result = model.invoke(prompt)

        return jsonify({'saran': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
