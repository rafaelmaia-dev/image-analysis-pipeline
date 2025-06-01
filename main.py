import requests
import base64
import json
import os
from dotenv import load_dotenv

load_dotenv()

IMG_URL = "<EXAMPLE_IMAGE_URL_OR_ID>"

API_URL = os.getenv("API_URL")
SUBMIT_URL = os.getenv("SUBMIT_URL")
AUTH_TOKEN = os.getenv("API_AUTH_TOKEN")

if not AUTH_TOKEN:
    raise ValueError("API_AUTH_TOKEN não definido no .env")

def analyze_image(image_path):
    """Analisa a imagem usando uma API externa"""
    try:
        print(f"[ETAPA 1] Analisando imagem {image_path}...")

        if not os.path.exists(image_path):
            print("[ERRO] Arquivo de imagem não encontrado!")
            return None

        with open(image_path, "rb") as f:
            image_data = base64.b64encode(f.read()).decode('utf-8')

        headers = {
            "Authorization": f"Bearer {AUTH_TOKEN}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "microsoft-florence-2-large",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "<DETAILED_CAPTION>"},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_data}"}}
                    ]
                }
            ],
            "max_tokens": 1000
        }

        response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        print("[SUCESSO] Análise concluída!")
        return response.json()

    except Exception as e:
        print(f"[ERRO CRÍTICO] Falha na análise: {str(e)}")
        return None

def submit_results(response_json):
    """Submete os resultados para a API"""
    try:
        print("[ETAPA 2] Submetendo resultados...")

        if not response_json:
            print("[ERRO] Nenhum dado para submeter!")
            return False

        headers = {
            "Authorization": f"Bearer {AUTH_TOKEN}",
            "Content-Type": "application/json"
        }

        response = requests.post(SUBMIT_URL, headers=headers, json=response_json, timeout=30)
        response.raise_for_status()
        print("[SUCESSO] Resposta submetida!")
        return True

    except Exception as e:
        print(f"[ERRO CRÍTICO] Falha na submissão: {str(e)}")
        return False

def main():
    print("=" * 50)
    print(" INÍCIO DO PROCESSO ".center(50, "="))
    print("=" * 50)

    image_path = "scraped_image.jpg"

    analysis = analyze_image(image_path)
    if not analysis:
        return

    if submit_results(analysis):
        print("\n[PROCESSO CONCLUÍDO COM SUCESSO]")
    else:
        print("\n[PROCESSO FINALIZADO COM ERROS]")

if __name__ == "__main__":
    main()
