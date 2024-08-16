import os
import json
import requests

headers = {"Authorization": f"Bearer {os.environ['HUGGINGFACEHUB_API_TOKEN']}"}
API_URL = "https://api-inference.huggingface.co/models/Davlan/distilbert-base-multilingual-cased-ner-hrl"


def query(payload):
    data = json.dumps(payload)
    response = requests.request("POST", API_URL, headers=headers, data=data)
    response.raise_for_status()
    return response.json()


def get_response_ner(text: str, tag: str):
    response = query({"inputs": f"{text}"})
    for res in response:
        if tag == res['entity_group']:
            return res['word']
    return None
