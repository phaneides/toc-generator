from config import GOOGLE_API_KEY
from google import genai
from google.genai import types
import os
import json

def generate_toc_from_images(FOLDER = "aux"):
# === CONFIGURACIÓN ===
    #FOLDER = "aux"
    MODEL_ID = "gemini-2.5-flash"
    thinking_budget = 0
    temperature = 0.4
    top_p = 0.95
    top_k = 20

# === CLIENTE GEMINI ===
    client = genai.Client(api_key=GOOGLE_API_KEY)

# === CARGAR ARCHIVOS DE IMAGEN ===
    image_files = sorted([
        f for f in os.listdir(FOLDER)
        if f.startswith("toc-") and f.endswith(".png")
    ], key=lambda x: int(x.split('-')[1].split('.')[0]))

# === PROMPT DE SISTEMA Y CONTENIDO ===
    contents = [
    """
    Extract the table of contents from the following scanned pages.

    Return only the structured data as a list of lists. Each item must follow the format:
    [hierarchy_level: int, title: str, page_number: int]

    Skip any section that is part of the front matter (e.g. prefaces, notation, etc).

    Hierarchy levels must begin at 1.

    Respect the declared data types above at all costs.
    """
    ]

# === ADJUNTAR IMÁGENES COMO PARTES ===
    for filename in image_files:
        path = os.path.join(FOLDER, filename)
        with open(path, 'rb') as f:
            contents.append(types.Part.from_bytes(data=f.read(), mime_type='image/png'))

# === CONSULTA A GEMINI CON FORMATO ESTRUCTURADO ===
    response = client.models.generate_content(
        model=MODEL_ID,
        contents=contents,
        config={
            "thinking_config": {
                "thinking_budget": thinking_budget,
            },
            "temperature": temperature,
            "top_p": top_p,
            "top_k": top_k,
            "response_mime_type": "application/json",
            "response_schema": list[list],  # fuerza el tipo: lista de listas
        },
    )

# === GUARDAR RESULTADO EN ARCHIVO ===
    toc_path = os.path.join(FOLDER, "toc.json")
    with open(toc_path, "w", encoding="utf-8") as f:
        json.dump(response.parsed, f, ensure_ascii=False, indent=2)

    print(f"[✔] Tabla de contenido guardada en: {toc_path}")

    return response.parsed
