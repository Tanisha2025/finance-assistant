# utils.py
import re

def clean_financial_text(text):
    # Extra spaces aur unwanted characters remove karega
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def validate_response(response, context):
    # Ek simple check: Kya AI ne jo number bola wo context mein hai?
    # (Optional logic for extra safety)
    pass