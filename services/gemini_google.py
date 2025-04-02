import os
import json
from google import genai
from google.genai import types
from services.gemini_interface import GeminiService
from models.company import CompanyQuery, FinancialInsights
from utilities.debug import debug_here
from dotenv import load_dotenv
from utilities.logger import get_logger

load_dotenv()

logger = get_logger(__name__)

class GeminiGoogleService(GeminiService):
    def __init__(self, api_key: str = None):

        api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not api_key:
            logger.exception("Please set the GEMINI_API_KEY environment variable. in logger {__name__}")
        
        self.client = genai.Client(api_key="AIzaSyD-Jn3FAIi7QIG7mHMm8f1RaYx66apV25k")
        self.model = self.client.models

    def get_analysis(self, prompt: str) -> str:

        model_version = os.getenv("GEMINI_VERSION")
        if not model_version:
            logger.exception("Please set the GEMINI_VERSION environment variable. in logger {__name__}")
        
        gen_config = types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=FinancialInsights,
        )
    
        response = self.model.generate_content(
            model=model_version, 
            contents=prompt, 
            config=gen_config
        )

        return response.text