import os
import base64
import pandas as pd
from openai import OpenAI
from pypdf import PdfReader
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def encode_image(uploaded_file):
    """Image ko AI ke samajhne layak format mein badalna"""
    return base64.b64encode(uploaded_file.getvalue()).decode('utf-8')

def get_file_content(uploaded_file):
    """PDF aur CSV se text nikalna"""
    text = ""
    if uploaded_file.name.endswith('.pdf'):
        reader = PdfReader(uploaded_file)
        for page in reader.pages:
            text += (page.extract_text() or "") + "\n"
    elif uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
        text = df.to_string()
    return text

def run_smart_ai(user_query, context_text="", image_base64=None):
    """Smart Assistant jo Text, Files aur Images teeno ko read karega"""
    try:
        messages = [
            {
                "role": "system",
                "content": (
                    "You are an Elite Multilingual Agent. "
                    "1. Respond in the EXACT language of the user. "
                    "2. If an image is provided, analyze it deeply (OCR + Visuals). "
                    "3. If a document text is provided, use it for smart answers. "
                    "4. Correct user typos automatically."
                )
            }
        ]
        
        # User message content (Text + Image support)
        user_content = [{"type": "text", "text": f"Context: {context_text}\n\nQuestion: {user_query}"}]
        
        if image_base64:
            user_content.append({
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}
            })
            
        messages.append({"role": "user", "content": user_content})

        response = client.chat.completions.create(
            model="gpt-4o", # Vision ke liye 'gpt-4o' zaroori hai
            messages=messages,
            temperature=0.3
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"AI Error: {str(e)}"