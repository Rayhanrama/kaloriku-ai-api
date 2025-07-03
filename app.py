from flask import Flask, request, jsonify
from langchain_community.llms import Replicate
import os

app = Flask(__name__)

model = Replicate(
    model="ibm-granite/granite-3.3-8b-instruct",
    replicate_api_token=os.environ.get('REPLICATE_API_TOKEN'),
    model_kwargs={"max_tokens": 1024, "temperature": 0.2},
)

def zeroshot_prompt_diet(data):
    return f"""
    Saya pengguna aplikasi diet bernama Kaloriku. Hari ini saya telah mengonsumsi {data['kalori_masuk']}kkal dan membakar {data['kalori_terbakar']}kkal.
    Target defisit saya {data['target_defisit']}kkal. Berikan saran makanan atau aktivitas tambahan yang ringkas dan mudah dipahami.
    """

@app.route('/saran-ai', methods=['POST'])
def saran_ai():
    data = request.json
    prompt = zeroshot_prompt_diet(data)
    result = model.invoke(prompt)
    return jsonify({'saran': result})
