import os
import json
import pdfplumber
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class PRExtractor:
    """Extracts structured Purchase Request data from PDFs using Gemini."""
    
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            print("WARNING: GEMINI_API_KEY not found in environment variables.")
        else:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-pro')

    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extracts raw text from a PDF file using pdfplumber."""
        text = ""
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() + "\n"
        return text

    async def extract_data(self, pdf_path: str) -> dict:
        """
        Extracts structured data from a PR PDF.
        Returns a dictionary with vendor, items, and totals.
        """
        raw_text = self.extract_text_from_pdf(pdf_path)
        
        prompt = f"""
        You are a Purchase Request Parser. 
        Extract the following data from the text below as a valid JSON object:
        - vendor_name (string)
        - pr_id (string)
        - date (string)
        - items (list of objects with: name, description, qty (number), unit_price (number), total_price (number))
        - grand_total (number)
        - currency (string, e.g. USD)

        Text:
        {raw_text}
        
        Return ONLY the JSON. No markdown formatting.
        """
        
        try:
            response = self.model.generate_content(prompt)
            # Basic cleanup if model returns markdown ticks
            cleaned_text = response.text.replace('```json', '').replace('```', '').strip()
            data = json.loads(cleaned_text)
            return data
        except Exception as e:
            print(f"Error extracting data with Gemini: {e}")
            # Fallback or error return
            return {"error": str(e), "raw_text": raw_text[:500]}
