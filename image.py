# image.py
import os
import PIL.Image
import google.generativeai as genai

def _config_genai():
    api_key = 'YOUR_API_KEY'
    if not api_key:
        raise RuntimeError("Set GEMINI_API_KEY env var.")
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-2.0-flash')

def get_text_from_image(file_path):
    """Extract text/description from an image using Gemini."""
    try:
        model = _config_genai()
        img = PIL.Image.open(file_path)
        resp = model.generate_content(img)
        return {"text": getattr(resp, "text", str(resp))}
    except Exception as e:
        return {"error": str(e)}
