import os
import torch
from flask import Flask, render_template, request, jsonify
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import warnings

MODEL_ID_GPU = "microsoft/Phi-3-mini-4k-instruct"
MODEL_ID_CPU = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

pipe = None
device = None
loaded_model_name = "Nenhum (Carregando...)"

def load_model():
    """
    Carrega o modelo e o pipeline do Hugging Face.
    - Se GPU (CUDA) estiver disponível: Carrega Phi-3 Mini com quantização 4-bit.
    - Se apenas CPU estiver disponível: Carrega TinyLlama (sem quantização).
    """
    global pipe, device, loaded_model_name

    if torch.cuda.is_available():
        device = "cuda:0"
        MODEL_ID = MODEL_ID_GPU
        loaded_model_name = "Microsoft Phi-3 Mini (GPU)"
        print(f"GPU detectada. Carregando: {MODEL_ID} com quantização 4-bit.")

        from transformers import BitsAndBytesConfig
        
        quantization_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_use_double_quant=True,
            bnb_4bit_compute_dtype=torch.bfloat16
        )
        
        model = AutoModelForCausalLM.from_pretrained(
            MODEL_ID,
            quantization_config=quantization_config,
            device_map=device,
            trust_remote_code=True,
            attn_implementation="eager"
        )
        
    else:
        device = "cpu"
        MODEL_ID = MODEL_ID_CPU
        loaded_model_name = "TinyLlama 1.1B (CPU)"
        print(f"Nenhuma GPU (CUDA) detectada. Carregando modelo CPU: {MODEL_ID}")
        warnings.warn(
            f"Usando {MODEL_ID} na CPU. A geração será mais rápida do que o Phi-3 na CPU, "
            "mas a qualidade da resposta pode ser menor."
        )
        
        model = AutoModelForCausalLM.from_pretrained(
            MODEL_ID,
            device_map=device,
            trust_remote_code=True
        )

    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)

    pipe = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
    )
    
    print(f"Modelo e pipeline carregados com sucesso: {loaded_model_name}")


app = Flask(__name__)

@app.route('/')
def index():
    """Serve a página principal."""
    return render_template('index.html')

@app.route('/api/model', methods=['GET'])
def get_model():
    """NOVO: Endpoint para informar o frontend sobre o modelo carregado."""
    return jsonify({"model_name": loaded_model_name})

@app.route('/generate', methods=['POST'])
def generate():
    """Endpoint da API para gerar texto. Esta função é STATELESS (sem memória)."""
    if pipe is None:
        return jsonify({"error": "Modelo não está carregado."}), 503

    try:
        data = request.get_json()
        prompt = data.get('prompt')
        
        if not prompt:
            return jsonify({"error": "Prompt não fornecido."}), 400

        template = f"""<|system|>
You are a helpful assistant.<|end|>
<|user|>
{prompt}<|end|>
<|assistant|>"""

        generation_args = {
            "max_new_tokens": 500,
            "return_full_text": False,
            "temperature": 0.1,
            "do_sample": True,
        }

        output = pipe(template, **generation_args)
        result = output[0]['generated_text']

        return jsonify({"response": result})

    except Exception as e:
        print(f"Erro durante a geração: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("Iniciando o carregamento do modelo...")
    load_model()
    print("Iniciando o servidor Flask...")
    app.run(host='0.0.0.0', port=5000, debug=False)