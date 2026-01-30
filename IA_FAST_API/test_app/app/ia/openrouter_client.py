import os
import httpx
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("API_KEY")
if not OPENROUTER_API_KEY:
    raise RuntimeError("API_KEY manquante dans le fichier .env")

OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "upstage/solar-pro-3:free")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
OPENROUTER_APP_NAME = os.getenv("OPENROUTER_APP_NAME", "MyCarApp")
OPENROUTER_SITE_URL = os.getenv("OPENROUTER_SITE_URL", "http://localhost:8000")


async def generate_car_description(brand: str, model: str, year: int) -> str:
    prompt = (
        f"Rédige uniquement une courte description commerciale en français pour "
        f"la voiture {brand} {model} sortie en {year}. "
        "Ne répète pas le prompt, pas d’instructions, juste la description finale, "
        "style marketing, quelques points clés comme performance, design, exclusivité."
    )


    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": OPENROUTER_SITE_URL,
        "X-Title": OPENROUTER_APP_NAME,
    }

    json_data = {
        "model": OPENROUTER_MODEL,
        "input": prompt,
        "max_output_tokens": 150,
    }

    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post(
            f"{OPENROUTER_BASE_URL}/responses",
            headers=headers,
            json=json_data,
        )
        response.raise_for_status()

        data = response.json()

        try:
            return data["output"][0]["content"][0]["text"]
        except (KeyError, IndexError):
            return "Pas de description générée"
